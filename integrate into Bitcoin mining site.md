Integration Architecture — Bitcoin Mining + ApexBEMS

A Bitcoin mining site has three layers.
Decisions flow top → bottom. Telemetry flows bottom → top.
Layer A — Physical Assets

ASICs, switchgear, battery system (PCS + BMS), site transformer, utility + internal metering.
Layer B — Control Plane

Miner management (LuxOS, Foreman, custom RPC), ApexBEMS as site EMS, SCADA (Modbus/BACnet), telemetry ingestion.
Layer C — Market & Optimization

ApexBEMS MPC engine, ensemble forecasting, bid‑curve generator, ISO market connectors (ERCOT, PJM, ISO‑NE, CAISO).

Contract: Layer C decides → Layer B executes → Layer A responds.
Integration Pipeline — Deterministic Steps
1. Expose Mining Load as a Controllable Variable

ApexBEMS requires a single control handle:
Code

P_MINE(t) = site mining power (kW)

Surfaced via Foreman API, LuxOS RPC, or direct ASIC frequency/voltage control.

ApexBEMS issues deterministic commands:

    Increase load by 3 MW

    Curtail to 0 MW for 5 minutes

    Ramp down 20% for regulation‑up headroom

Gate: If mining load cannot be directly controlled, integration stops here.
2. Add Mining Load to the MPC Optimization

Introduce a mining decision variable:
Code

P_MINE[t] ∈ [0, P_MINE_MAX]

Extend the site power balance:
Code

P_GRID[t] = P_BATT[t] + P_MINE[t]

One optimization problem.
No competing loops.
No oscillations.
3. Price Mining Economics into the Objective Function

Mining reduces to a marginal kWh value:
Code

value_per_kwh = (BTC_price × sats_per_kwh) − energy_cost_per_kwh

Update the objective:
Code

maximize Σₜ [
    market_revenue(t)
  + mining_value(P_MINE[t])
  − battery_degradation(t)
  − imbalance_penalties(t)
]

Pivot: Mining becomes a price‑responsive flexible asset, not a static load.
4. Wire ApexBEMS to the Miner Control API

Add an EventBus subscriber:
Code

event_type = "dispatch_decision"
callback  = send_to_miner_manager

The callback translates P_MINE[t] into:

    ASIC frequency commands

    Pool‑side throttles

    Miner‑manager group instructions

Stateless. Deterministic. One direction.
No polling. No reconciliation.
5. Wire ApexBEMS to the Battery PCS

PCS interfaces: Modbus TCP, SunSpec, CAN‑to‑TCP gateways, vendor REST APIs.

Map:
Code

P_BATT[t] → charge/discharge setpoints

ApexBEMS already owns SOC tracking, temperature, and SOS2 degradation curves.
The PCS simply executes.
6. Connect ApexBEMS to the ISO Market

Configure:
Code

market   = "ERCOT"
products = ["energy", "reg_up", "reg_down", "spin"]

ApexBEMS provides:

    bid‑curve generator

    PolicyValidator

    market client with retry logic

    imbalance penalty modeling

Mining + battery operate as a single VPP from the ISO’s perspective.
7. Feed Mining Telemetry into the Forecasters

Provide real‑time streams of:

    Hashrate

    Miner temperature

    Miner efficiency (J/TH)

    Pool difficulty

    BTC price

    Transaction fee rate

These sharpen curtailment timing, mining‑vs‑arbitrage tradeoffs, and volatility‑aware horizon adjustment.
The ensemble consumes them directly — no transformation layer needed.
What This Unlocks
Mining becomes a grid service

Frequency regulation. Ramping reserves. Congestion relief. Real‑time balancing.
Same ASICs, new revenue streams.
Battery + mining = maximum arbitrage

Mine when cheap.
Discharge when expensive.
Curtail at negative prices.
Charge before volatility.
Sell flexibility into ancillary markets.
One optimizer, five degrees of freedom.
Mining becomes anti‑fragile

ApexBEMS predicts volatility, adapts its horizon, logs shadow prices, explains decisions, persists state, and recovers from corruption.
Operations don’t break — they adapt.
Integration Checklist
Code

☐ Expose P_MINE(t) as a controllable variable
☐ Add P_MINE[t] to MPC model + power balance
☐ Add mining marginal value to the objective function
☐ Connect miner manager to EventBus ("dispatch_decision")
☐ Connect battery PCS to ApexBEMS dispatch commands
☐ Feed BTC price + mining telemetry into forecasters
☐ Enable ISO bid‑curve submission
☐ Validate all bids through PolicyValidator
☐ Run MPC loop at 5‑minute cadence
☐ Confirm shadow prices reflect mining opportunity cost
