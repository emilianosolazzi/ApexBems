Integration architecture — Bitcoin mining + ApexBEMS

A Bitcoin mining site has three layers. Integration means deterministic control flowing top → bottom, telemetry flowing bottom → top.

Layer A — Physical assets  
ASICs, switchgear, battery system (PCS + BMS), site transformer, utility and internal metering.

Layer B — Control plane  
Miner management (LuxOS, Foreman, custom RPC), ApexBEMS as the battery + site EMS, site SCADA (Modbus/BACnet), telemetry ingestion pipeline.

Layer C — Market & optimization  
ApexBEMS MPC engine, ensemble forecasting, bid curve generator, market API connectors (ERCOT, PJM, ISO‑NE, CAISO).

Integration rule: Layer C decides, Layer B executes, Layer A responds.
The integration pipeline — step by step
Step 1 — Expose mining load as a controllable variable

ApexBEMS needs a single control handle:
text

P_MINE(t) = site mining power in kW

Surfaced via Foreman API, LuxOS RPC, or direct ASIC frequency/voltage control. ApexBEMS issues commands like:

    “Increase load by 3 MW”

    “Curtail to 0 MW for 5 minutes”

    “Ramp down 20% for regulation‑up headroom”

If ApexBEMS cannot directly command mining load, integration stops here. This is non‑negotiable.
Step 2 — Add mining load to the MPC optimization

Introduce a mining decision variable:
text

P_MINE[t] ∈ [0, P_MINE_MAX]

Extend the site power balance:
text

P_GRID[t] = P_BATT[t] + P_MINE[t]

Now the solver can jointly decide: mining, charging, discharging, curtailment, and ancillary provision in one optimization problem—no competing control loops.
Step 3 — Price mining economics into the objective function

Reduce mining economics to a marginal value per kWh:
text

value_per_kwh = (BTC_price × sats_per_kwh) − energy_cost_per_kwh

Update the ApexBEMS objective:
text

maximize Σₜ [
    market_revenue(t)
  + mining_value(P_MINE[t])
  − battery_degradation(t)
  − imbalance_penalties(t)
]

Without this, mining is just background load. With it, mining becomes a price‑responsive flexible asset traded against battery dispatch and market signals.
Step 4 — Wire ApexBEMS to the miner control API

Use the existing EventBus and add a subscriber:
text

event_type = "dispatch_decision"
callback  = send_to_miner_manager

The callback maps P_MINE[t] into ASIC frequency commands, pool‑side throttles, or miner‑manager group instructions. Stateless, deterministic, one‑way: no polling, no state reconciliation.
Step 5 — Wire ApexBEMS to the battery PCS

Most PCS systems speak Modbus TCP, SunSpec, CAN‑to‑TCP, or vendor REST APIs. Map:
text

P_BATT[t] → charge/discharge setpoints

ApexBEMS already handles SOC, temperature, SOS2 degradation, and cost curves. The PCS only needs to follow setpoints.
Step 6 — Connect to the ISO market

Configure the built‑in market stack:
text

market   = "ERCOT"
products = ["energy", "reg_up", "reg_down", "spin"]

ApexBEMS uses its bid curve generator, PolicyValidator, market client, retry logic, and imbalance modeling. Mining + battery operate as a single VPP, no extra coordination layer.
Step 7 — Feed mining telemetry into the forecasters

Provide real‑time streams of:

    Hashrate

    Miner temperature

    Miner efficiency (J/TH)

    Pool difficulty

    BTC price

    Transaction fee rate

These features sharpen curtailment, mining‑vs‑arbitrage decisions, and volatility‑aware horizon adjustment. The ensemble forecaster can consume them directly.
What this unlocks

Mining becomes a grid service  
Frequency regulation, ramping reserves, congestion relief, real‑time balancing—the same ASICs that secure Bitcoin now stabilize the grid.

Battery + mining = maximum arbitrage  
The optimizer continuously selects the highest‑value mix: mine when cheap, discharge when expensive, curtail at negative prices, charge ahead of volatility, sell flexibility into ancillary markets. This is energy trading with ASICs attached.

Mining becomes anti‑fragile  
ApexBEMS predicts volatility, adapts its horizon, logs shadow prices, explains decisions, persists state, and recovers from corruption. Operations don’t break on edge cases—they adapt.
Integration checklist
text

☐ Expose P_MINE(t) as a controllable variable
☐ Add P_MINE[t] to the MPC model and power balance
☐ Add mining marginal value to the objective function
☐ Connect miner manager to EventBus ("dispatch_decision")
☐ Connect battery PCS to ApexBEMS dispatch commands
☐ Feed BTC price + mining telemetry into forecasters
☐ Enable bid curve submission to ISO
☐ Validate all bids through PolicyValidator
☐ Run MPC loop at 5-minute cadence
☐ Verify shadow prices reflect mining opportunity cost
