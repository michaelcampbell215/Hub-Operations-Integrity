# Hub Operations Integrity & Recovery Simulation
#### Multi-Constraint Decision Intelligence | Cost Optimization Under Regulatory Constraints | $122K Net Savings

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Methodology](https://img.shields.io/badge/Methodology-Multi--Constraint_Optimization-orange.svg)](https://en.wikipedia.org/wiki/Constraint_programming)
[![Domain](https://img.shields.io/badge/Domain-Operations_Analytics-0D6EFD.svg)](https://en.wikipedia.org/wiki/Operations_research)

> [!IMPORTANT]
> **Executive Summary:** This simulation quantifies the cost of every operational decision during a systemic hub disruption. By modeling a 4-hour recovery window against real regulatory constraints, the system identified **$122,342.50 in net operational savings**, protected **12 downstream flight legs** from cascading failures, and cleared a **370-bag backlog** by utilizing latent payload capacity — transforming intuition-based gate decisions into a data-driven command framework.

---

> [!NOTE]
> **Supply Chain & Operations Analytics Connection:** The analytical framework here — multi-constraint cost modeling, network integrity analysis, and regulatory guardrail enforcement — translates directly to complex operations analytics roles in logistics networks, healthcare supply chain distribution hubs, and global fulfillment operations where regulatory compliance and cascading failure risk must be modeled simultaneously. The MCT Cliff model maps to carrier SLA penalty structures; PPBM logic maps to inventory reconciliation; Fill-the-Bin capacity optimization maps to load planning in any distribution environment.

> [!NOTE]
> **Analytics Engineering Connection:** This project demonstrates production-grade Python engineering patterns: JSON manifest ingestion, custom multi-constraint cost functions with non-linear penalty curves, regulatory guardrail logic as hard overrides, and simulation output visualization via Matplotlib. The architecture — ingest, classify, score, optimize, output — is directly transferable to data pipeline and decision support engineering roles.

---

## The Problem

In high-stakes operations, individual decisions have network-wide consequences that are invisible without explicit cost modeling. Operations teams relying on intuition routinely make "Push Now" decisions that appear correct at the gate level but trigger cascading failures — missed connections, crew duty limit violations, downstream cancellations — that cost multiples of what a strategic hold would have.

This project builds a decision support framework that determines the **precise break-even point** for every hold vs. push decision during a systemic hub disruption, enforcing regulatory guardrails as hard constraints rather than guidelines.

## Data & Methodology

**Data Sources:**
- **Primary Data:** A custom JSON-based manifest representing 10 narrow-body departures (A319/A320/A321) during a simulated disruption event.
- **Parameters:** Real-world constraints derived from 10 years of American Airlines operations — Empty Operating Weights (EOW), Maximum Zero Fuel Weights (MZFW), and FAA Part 117 crew duty limits.

**Process:**
1. **Ingestion:** Parsed complex gate manifests to classify Local No-Shows (bags already in pit, requiring search) vs. Security Stalls (bags not yet at gate) — two operationally distinct problems requiring fundamentally different responses.
2. **Cost Analysis:** Applied a non-linear MCT Cliff model where delay costs spike at the 15 and 30-minute marks to account for downstream misconnect exposure.
3. **Simulation:** Ran a multi-variable comparison per flight: *Cost of Passenger Protection vs. Cost of Hold + Crew Duty Risk + Gate Conflict*.
4. **Optimization:** Applied Fill-the-Bin logic to authorize up to 50 backlogged bags per flight based on real-time weight and balance availability.

## Technical Pivot

**From Linear Calculator to Multi-Constraint Network Model**

The project evolved from a simple cost-of-delay calculator once it became clear that pushing on-time often creates hidden, systemic downstream costs that a linear model cannot capture.

- **Physical Rework Integration:** Incorporated Strict Positive Passenger Bag Match (PPBM) logic to model mandatory baggage-offload delays — proving that a "Push Now" decision can yield a *longer* net delay than a strategic 15-minute hold when high-density cargo pits require a 7-minute search.
- **Regulatory Guardrails as Hard Overrides:** Integrated FAA Part 117 duty limit logic to trigger Force Push orders whenever a strategic hold threatened crew legal flying windows. Individual gate decisions cannot be made without knowing crew duty exposure.
- **Gate Occupancy as Network Resource:** Factored in $180/min tarmac fuel burn and DOT tarmac risk for inbound aircraft waiting on occupied departure gates — treating gate capacity as a finite, network-wide constraint rather than a local variable.

## Key Insights

- **The Network Integrity Premium:** Enforcing FAA Part 117 compliance over individual flight recovery mitigated an estimated **$50,000 in potential cancellation costs**. Individual gate decisions are network decisions.
- **The Rework Density Paradox:** A 15-minute hold for 25 passengers is often faster than a Push Now requiring a 70-minute bag search for 10 local no-shows. The math must be done explicitly — intuition fails in high-density cargo configurations.
- **Cargo ROI:** The marginal fuel cost of clearing 370 backlogged bags was approximately $375 compared to approximately $37,500 in avoided courier fees — a 100x return on operational hold time.

## Recommendations

1. **High-Yield Segment Prioritization:** Long-haul flight profiles require protective holding strategies — re-accommodation options are limited and protection costs exceed $1,000 per passenger. The model quantifies exactly when holding becomes the cheaper decision.
2. **Predictive Regulatory Compliance:** Implement automated monitoring of `duty_mins_remaining` to provide gate agents with hard-stop departure windows before crew duty limits become a cascading network constraint.
3. **Cargo Expedite as Standard Protocol:** The Fill-the-Bin analysis establishes that backlog clearance is almost always financially justified during disruption windows — this should be a standing operating procedure, not a judgment call.

## Next Steps

- **Dynamic Weather & De-Icing Variables:** Incorporate station-specific de-icing throughput and taxi-out variance to adjust break-even gate hold thresholds during winter operations.
- **Live Telemetry & API Integration:** Transition from static JSON manifests to live data feeds with real-time TSA wait time integration.
- **Multi-Hub Conflict Modeling:** Expand gate occupancy logic to include downstream gate availability — preventing hold decisions at one hub that create tarmac gridlock at a gate-saturated destination.
- **ML No-Show Probability:** Build a predictive model for security-stall probability to enable earlier standby clearance and baggage expedite decisions before the T-10 departure cutoff.