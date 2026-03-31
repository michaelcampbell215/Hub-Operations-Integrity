# Digital Twin: PHL Hub Operations Integrity & Recovery Simulation
**Decision Intelligence for Critical Airline Gate Management.**
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)

> [!IMPORTANT]
> **Executive Summary**  
> During a simulated 4-hour window of a systemic hub disruption (March 2026), this model identified **$122,342.50** in net operational savings. By balancing passenger protection costs against a Regulatory Guardrail logic, the simulation protected **12 downstream flight legs** from cascading cancellations and cleared a **370-bag backlog** using latent aircraft capacity.

---

## Project Overview
In airline operations, the Turn is a high-precision workflow. This project analyzes the systemic disruption caused by the 2026 Government Shutdown, specifically quantifying the operational impact of security bottlenecks at Philadelphia International Airport (PHL). The goal was to build a decision support tool that moves beyond intuition to determine the precise break-even points for hub recovery and network integrity.



## Data & Methodology

### Data Sources
*   **Primary Data**: A custom JSON-based manifest representing 10 narrow-body departures (A319, A320, A321).
*   **Parameters**: Real-world constraints derived from 10 years of experience at American Airlines, including Empty Operating Weights (EOW), Maximum Zero Fuel Weights (MZFW), and FAA Part 117 duty limits.

### Process
1.  **Ingestion**: Parsed complex gate sheets to identify Local No-Shows (bags in pit) vs. Security Stalls (bags not yet loaded).
2.  **Cost Analysis**: Applied a non-linear MCT Cliff model where delay costs spike at the 15 and 30-minute marks to account for hub misconnects.
3.  **Simulation**: Ran a multi-variable comparison for every flight: *Cost of Protection vs. Cost of Hold + Crew Risk + Gate Conflict*.
4.  **Optimization**: Utilized a Fill-the-Bin logic to authorize up to 50 backlogged bags per flight based on real-time weight and balance availability. In production, this is a variable rate based on individual flight parameters and dispatch enforced constraints.


## Technical Pivot
The project evolved from a linear cost-of-delay calculator into a Dynamic Hub Ecosystem upon identifying that an on-time push often incurs hidden, systemic costs. This shift moved the architecture from siloed flight analysis to a Multi-Constraint Network Model.

*   **Physical Rework Integration**: Incorporated Strict Positive Passenger Bag Match (PPBM) logic to account for mandatory baggage-offload delays. This recognized the Rework Penalty, specifically the 7-minute search latency required to extract bags from high-density AFT cargo pits proving that a Push Now can often yield a longer net delay than a strategic 15-minute hold.

*   **Regulatory Guardrails**: Integrated FAA Part 117 duty limits to trigger a Force Push whenever a strategic hold threatened a crew’s legal flying window. This prioritized downstream network stability and avoided $50,000+ in potential crew-related cancellation costs.

*   **Gate Occupancy Modeling**: Factored in the $180/min tarmac fuel burn and DOT risk for inbound aircraft waiting on a departure gate. This treated Gate Fluidity as a finite resource, preventing taxiway gridlock during peak arrival banks.



## Key Insights

*   **The Network Integrity Premium**: Prioritizing FAA Part 117 compliance over individual segment recovery mitigated an estimated $50,000 in potential cancellation costs. This highlights the strategic necessity of enforcing strict departure cutoffs to safeguard the broader network.
*   **Rework Density**: A 15-minute hold for 25 passengers is often faster than a Push Now that requires a 70-minute bag search for 10 local no-shows.
*   **Cargo ROI**: The marginal fuel cost of clearing 250+ bags was negligible ($\approx \$375$) compared to the massive savings in avoided courier fees ($\approx \$37,500$).


## Recommendations & Next Steps

### Strategic Recommendations
1.  **High-Yield Segment Prioritization**: Simulation data confirms that transcontinental and long-haul flight profiles (e.g., LAX, SFO) require a protective holding strategy. Due to limited re-accommodation frequency and protection costs exceeding $1,000 per passenger, the ROI of a strategic gate hold on these segments significantly outweighs the marginal cost of network delay.

2.   **Predictive Regulatory Compliance**: Implement automated monitoring of the `duty_mins_remaining` variable to establish Hard-Stop Departure Windows. By providing gate operations with a real-time countdown to Part 117 duty limits, the hub can systematically eliminate the $50,000+ financial impact of crew-related cancellations.


## Action Plan
*   **Dynamic Weather & De-Icing Variables**: Incorporate station-specific de-icing throughput and taxi-out variance. This allows the model to adjust the break-even point for gate holds during Winter Operations, where ground time is at a premium.

*   **Live Telemetry & API Integration**: Transition from static JSON manifests to live data feeds (e.g., SABRE, FlightAware, or internal Crew Management Systems). Integrating real-time TSA Wait Time APIs would allow for predictive passenger flow modeling before the gate agent even identifies a no-show.

*   **Fuel Burn & Performance Precision**: Refine the Cost of Weight logic by integrating specific Aircraft Tail Number performance data. By calculating the exact fuel burn differential for an A321-200 on a high-altitude PHL-PHX route versus a short-haul PHL-CLT segment, the model ensures maximum accuracy in cargo-fill authorization.

*   **Multi-Hub Conflict Modeling**: Expand the Gate Occupancy logic to include Downstream Gate Availability. This prevents Holding for Pax in PHL only to arrive at a Gate-Saturated hub like DFW, which would result in additional tarmac delays and network friction.

*   **Machine Learning for No-Show Probability**: Move from a binary checked-in vs. boarded count to a predictive model. By analyzing historical security-stall data, the system can predict the likelihood of a passenger making the flight before the T-10 cutoff, allowing for earlier standby clearance and baggage expedite decisions.
