Integration Architecture — Bitcoin Mining + ApexBEMS

A Bitcoin mining site has three layers. Integration means connecting them with deterministic control flowing top to bottom, telemetry flowing bottom to top.

Layer A — Physical Assets
ASICs, switchgear, battery system (PCS + BMS), site transformer, utility and internal metering.

Layer B — Control Plane
Miner management (LuxOS, Foreman, custom RPC), ApexBEMS as the battery EMS, site SCADA (Modbus/BACnet), telemetry ingestion pipeline.

Layer C — Market & Optimization
ApexBEMS MPC engine, ensemble forecasting, bid curve generator, market API connectors (ERCOT, PJM, ISO-NE, CAISO).

Integration is simple: Layer C decides, Layer B executes, Layer A responds.
The Integration Pipeline — Step by Step
Step 1 — Expose Mining Load as a Controllable Variable

ApexBEMS needs a single control handle:
text

P_mine(t) = site mining power in kW

This is surfaced through Foreman API, LuxOS RPC, or direct ASIC frequency/voltage control. ApexBEMS sends commands like:

    "Increase load by 3 MW"

    "Curtail to 0 MW for 5 minutes"

    *"Ramp down 20% for regulation-up headroom"*

If ApexBEMS can't talk directly to the miners, integration stops here. This is non-negotiable.
Step 2 — Add Mining Load to the MPC Optimization

Inside the optimization model, add:
text

P_MINE[t] ∈ [0, P_MINE_MAX]

And extend the site power balance:
text

P_GRID[t] = P_BATT[t] + P_MINE[t]

Now the solver can simultaneously decide: mine, charge, discharge, curtail, and provide ancillary services — all in one unified problem. No separate control loops fighting each other.
Step 3 — Price Mining Economics into the Objective Function

Mining profitability decomposes to a single marginal value per kWh:
text

value_per_kwh = (BTC_price × sats_per_kwh) − energy_cost_per_kwh

The ApexBEMS objective becomes:
text

maximize Σₜ [
    market_revenue(t)
  + mining_value(P_MINE[t])
  − battery_degradation(t)
  − imbalance_penalties(t)
]

This is the critical step. Without it, ApexBEMS treats mining as background load. With it, mining becomes a price-responsive flexible asset that the optimizer can trade against battery dispatch and market signals.
Step 4 — Wire ApexBEMS to the Miner Control API

ApexBEMS already has an EventBus. Add a subscriber:
text

event_type = "dispatch_decision"
callback  = send_to_miner_manager

The callback translates P_MINE[t] into ASIC frequency commands, pool-side throttle signals, or miner-manager group instructions. Stateless, deterministic, single-direction. No polling. No state reconciliation.
Step 5 — Wire ApexBEMS to the Battery PCS

Most PCS systems speak Modbus TCP, SunSpec, CAN-to-TCP gateways, or vendor REST APIs. Map P_BATT[t] to charge/discharge setpoints.

ApexBEMS already handles SOC tracking, temperature, degradation (SOS2), and cost curves. The PCS just needs to obey.
Step 6 — Connect to the ISO Market

ApexBEMS ships with a bid curve generator, policy validator, market API client, retry logic, and imbalance penalty modeling. Configure:
text

market   = "ERCOT"
products = ["energy", "reg_up", "reg_down", "spin"]

Mining + battery becomes a single market-participating VPP. No external coordination layer required.
Step 7 — Feed Mining Telemetry into the Forecasters

Give ApexBEMS real-time streams of:

    Hashrate

    Miner temperature

    Miner efficiency (J/TH)

    Pool difficulty

    BTC price

    Transaction fee rate

These features sharpen curtailment decisions, mining-vs-arbitrage tradeoffs, and volatility-aware horizon adjustment. The ensemble already knows how to consume them.
What This Unlocks
Mining becomes a grid service

Frequency regulation, ramping reserves, congestion relief, real-time balancing. The same ASICs that secure the network now stabilize the grid.
Battery + mining = maximum arbitrage

The optimizer continuously selects the highest-value combination: mine when cheap, discharge when expensive, curtail at negative prices, charge before volatility, sell flexibility into ancillary markets. This is energy trading with ASICs attached.
Mining becomes anti-fragile

ApexBEMS predicts volatility, adapts its horizon, logs shadow prices, explains its decisions, persists state across restarts, and recovers from corruption. Operations don't break on edge cases. They adapt.
Integration Checklist
text

☐ Expose P_mine(t) as a controllable variable
☐ Add P_MINE[t] to the MPC model and power balance
☐ Add mining marginal value to the objective function
☐ Connect miner manager to EventBus ("dispatch_decision")
☐ Connect battery PCS to ApexBEMS dispatch commands
☐ Feed BTC price + mining telemetry into forecasters
☐ Enable bid curve submission to ISO
☐ Validate all bids through PolicyValidator
☐ Run MPC loop at 5-minute cadence
☐ Verify shadow prices reflect mining opportunity cost

