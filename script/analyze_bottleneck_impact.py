import json
import os

# DATA INITIALIZATION
def load_and_init(json_data):
    meta = json_data['metadata']
    flights = json_data['flights']
    fc = meta['financial_constants']
    oc = meta['operational_constants']
    return fc, oc, flights

def load_json_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Pathing to gate_sheet_data.json
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(SCRIPT_DIR, "..", "data", "gate_sheet_data.json")

data = load_json_file(DATA_PATH)


# COST MODELING: NETWORK RISK (DELAY + CONNECTIONS + CREW)
def calculate_network_risk(mins, onboard_pax, crew_risk, fc):
    base_delay_cost = mins * fc['cost_of_delay_per_min']
    
    # 1. The MCT Cliff (Connection Risk)
    multiplier = 1.0
    if 15 < mins <= 30: multiplier = 2.5
    elif mins > 30: multiplier = 5.0
    
    connection_penalty = (onboard_pax * fc['missed_connection_penalty_per_pax']) * (mins / 60)
    
    return base_delay_cost + (connection_penalty * multiplier) + crew_risk

# SHARED UTILITIES
def time_to_mins(time_str):
    h, m = map(int, time_str.split(':'))
    return h * 60 + m

def calculate_gate_conflict_cost(hold_time, flight, fc):
    # Calculate when the inbound wants the gate
    current_std_mins = time_to_mins(flight['STD'])
    inbound_eta_mins = time_to_mins(flight['next_inbound']['ETA'])
    inbound_arrival_delta = inbound_eta_mins - current_std_mins
    
    # Gate availability after hold + turn buffer
    gate_clear_mins = hold_time + fc['gate_turn_buffer_mins']
    tarmac_wait_mins = max(0, gate_clear_mins - inbound_arrival_delta)
    
    return tarmac_wait_mins * fc['tarmac_delay_cost_per_min']

def calculate_crew_timeout_risk(hold_time, crew_data, fc):
    remaining_buffer = crew_data['duty_mins_remaining'] - hold_time
    
    # The "Red Zone": 10 minutes or less of buffer
    if remaining_buffer <= 10:
        # Base timeout cost + penalty for every leg that gets cancelled after
        total_impact = fc['cost_of_crew_timeout'] + (crew_data['downstream_legs'] * fc['downstream_cancellation_buffer'])
        return total_impact
    
    # The "Yellow Zone": 11-20 minutes of buffer
    elif remaining_buffer <= 20:
        return 5000 # "Anxiety Cost" - Potential for a sub-out or extra paperwork
        
    return 0 # Green Zone: Crew is safe


# GATE CLOSURE & PPBM
def finalize_gate_ops(flight, oc):
    pax = flight['pax_data']
    manifest = flight['baggage_manifest']
    standbys = flight['standby_counts']

    # Identify Local No-Shows (Bags are on board = Must Pull)
    local_no_shows = pax['booked'] - pax['boarded'] - pax['security_delayed']
    security_stalls = pax['security_delayed']
    
    # Calculate Rework Delay (5 mins per bag search in the pit)
    bags_to_offload = max(0, local_no_shows)
    
    search_rate = 7 if manifest['pit_location'] == "AFT" else 3
    rework_delay = bags_to_offload * search_rate

    # Clear Standbys (RV > SA1)
    total_seats_to_fill = local_no_shows + security_stalls
    rv_cleared = min(total_seats_to_fill, standbys['RV'])
    sa1_cleared = min(total_seats_to_fill - rv_cleared, standbys['SA1'])
    total_standbys = rv_cleared + sa1_cleared
    final_pax_count = pax['boarded'] + total_standbys

    return {
        "final_pax": final_pax_count,
        "rework_mins": rework_delay,
        "bags_to_offload": bags_to_offload,
        "total_standbys": total_standbys,
        "security_stalls": security_stalls
    }


# RESOURCE OPTIMIZATION (EXPEDITE BAGS)
# We use the 'Latent Capacity' created by the no-shows to clear the bag room backlog.
# The 'max_expedite_limit' is set by the Dispatcher prior to loading (MLW/MTOW constraints).
def optimize_expedite(flight, final_pax, oc, fc):
    max_fwd_pieces = 60 
    current_fwd = 10 
    available_volume = max(0, max_fwd_pieces - current_fwd)

    # Weight & Volume Check
    pax_wt = final_pax * oc['avg_pax_weight_lbs']
    bag_wt = flight['baggage_manifest']['on_board_count'] * oc['avg_bag_weight_lbs']
    current_zfw = 106500 + pax_wt + bag_wt 
    
    wt_capacity_lbs = oc['max_A321_ZFW_lbs'] - current_zfw
    wt_limit_bags = int(wt_capacity_lbs / oc['avg_bag_weight_lbs'])
    
    # Authorize bags (Cannot exceed Dispatcher Limit or Aircraft Physical Volume)
    dispatcher_limit = flight.get('max_expedite_limit', 50)
    bags_auth = min(available_volume, wt_limit_bags, dispatcher_limit) 
    
    # Net Profit
    fuel_impact = (bags_auth * oc['avg_bag_weight_lbs']) * 0.05
    recovery_savings = bags_auth * fc['cost_of_mishandled_bag']
    net_savings = recovery_savings - fuel_impact

    return bags_auth, net_savings


# MAIN EXECUTION LOOP
fc, oc, flights = load_and_init(data)

total_savings = 0
total_bags_pulled = 0
total_standbys_cleared = 0
total_expedite_cleared = 0

fc, oc, flights = load_and_init(data)

total_savings = 0
total_bags_pulled = 0
total_standbys_cleared = 0
total_expedite_cleared = 0

print(f"{'FLIGHT':<8} | {'DEST':<5} | {'DECISION':<10} | {'PULLS':<5} | {'STBY':<4} | {'EXPD'} | {'SAVINGS':<8} | {'WARNING'}")
print("-" * 105)

for f in flights:
    ops = finalize_gate_ops(f, oc)
    unit_protect_cost = f.get('protection_cost_per_pax', fc['cost_of_protection_per_pax'])
    protect_cost = ops['security_stalls'] * (unit_protect_cost + fc['cost_of_mishandled_bag'])
    
    # 1. Decision Logic
    justification = ""
    conflict_cost = calculate_gate_conflict_cost(15, f, fc)
    
    # Calculate potential pulls if we push
    local_no_shows = f['pax_data']['booked'] - f['pax_data']['boarded'] - f['pax_data']['security_delayed']
    potential_pulls = max(0, local_no_shows + ops['security_stalls'])

    if 15 > f['crew_duty']['duty_mins_remaining']:
        decision, final_delay = "FORCE PUSH", ops['rework_mins']
        bags_offloaded = potential_pulls
        savings = 0
    else:
        crew_risk = calculate_crew_timeout_risk(15, f['crew_duty'], fc) 
        hold_cost_base = calculate_network_risk(15, f['pax_data']['boarded'], crew_risk, fc)
        total_hold_cost = hold_cost_base + conflict_cost
        
        if protect_cost > total_hold_cost:
            decision, final_delay = "HOLD 15M", 15
            bags_offloaded = max(0, local_no_shows) # Only pull the ghosts
            savings = protect_cost - total_hold_cost
        else:
            decision, final_delay = "PUSH NOW", ops['rework_mins']
            bags_offloaded = potential_pulls
            savings = 0
            if protect_cost > hold_cost_base:
                justification = "! TARMAC !"

    # 2. Capacity Recovery
    exp_bags, exp_savings = optimize_expedite(f, ops['final_pax'], oc, fc)
    
    # 3. Aggregate Metrics
    total_savings += (savings + exp_savings)
    total_bags_pulled += bags_offloaded
    total_standbys_cleared += ops['total_standbys']
    total_expedite_cleared += exp_bags
    
    print(f"{f['flight_number']:<8} | {f['destination']:<5} | {decision:<10} | {bags_offloaded:>5} | {ops['total_standbys']:>4} | {exp_bags:>4} | ${savings + exp_savings:^8,.0f} | {justification}")

print("-" * 105)
print(f"SUMMARY: ${total_savings:,.2f} Net Savings | {total_bags_pulled} Bags Pulled | {total_standbys_cleared} Standbys | {total_expedite_cleared} Expedites")