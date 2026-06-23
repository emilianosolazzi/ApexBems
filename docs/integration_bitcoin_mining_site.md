# Integration Architecture: Bitcoin Mining Site + ApexBEMS

This document describes the target integration architecture for a Bitcoin mining site. It distinguishes what the current repository already implements from what must still be built.

Current verified claim:

> ApexBEMS is a test-covered, public-data benchmarked, shadow-mode energy optimization engine with safety-gated dispatch recommendations and replayable audit logs.

## Current Status

Implemented today:

- Battery state tracking.
- Price-driven stochastic optimization.
- Bid curve generation.
- Policy validation.
- Battery dispatch validation through the current `SafetyGateway`.
- Shadow-mode defaults.
- Market submission blocked by default.
- SQLite audit logging.
- Replayable decision context and stable JSON hashes.
- Metrics counters for optimizer success/failure, safe fallback, SOC clipping, and SOC violations.
- EventBus.
- Simulated market client.
- Modular `apex_bems` package for new development.
- JSON Schema contract files and schema validation helpers.
- Test suite for core behavior, production hardening, public benchmark mechanics, schema examples, and legacy-vs-modular parity.
- Public benchmark runner using live ERCOT prices and public Bitcoin network signals.

Verified local snapshot:

- Pytest: `79 passed`.
- Public benchmark: `66` ERCOT `hbHubAvg` real-time intervals.
- Optimizer success rate: `100.00%`.
- Optimizer failures: `0`.
- Safe fallback intervals: `0`.
- SOC violations before clipping: `0`.

Not implemented yet:

- Live miner manager connector.
- Live PCS connector.
- ISO market connector.
- Full live schema adapter layer.
- Mining load as an optimization decision variable.
- Read-only shadow-mode connector for actual site telemetry.
- Signed dry-run PCS/miner command output.
- Hardware-in-the-loop validation.

## Site Layers

```text
Layer C: Market and optimization
  ApexBEMS MPC engine, forecasts, bid curves, policy validation,
  battery SafetyGateway, audit log, metrics

Layer B: Control plane
  Miner manager, PCS/BMS gateway, SCADA, telemetry ingestion,
  dry-run command adapters

Layer A: Physical assets
  ASICs, switchgear, battery, transformer, meters
```

Shadow-mode decision flow:

```text
Layer C recommends -> Layer B validates/dry-runs -> Operator reviews -> Layer A unchanged
```

Future staged-control flow:

```text
Layer C recommends -> Layer B validates -> Operator/automation approval -> Layer A executes
```

Telemetry flow:

```text
Layer A measures -> Layer B normalizes -> Layer C optimizes
```

## Integration Contracts

The `schemas/` folder defines the external payload shapes:

- `Mining-Telemetry.py`
- `Battery-Telemetry.py`
- `Market Price & Forecast Feed.py`
- `BTC + Fee Market Feed.py`
- `Unified Site Telemetry Envelope.py`
- `ApexBEMS-Mining Control.py`
- `ApexBEMS -PCS.py`
- `ApexBEMS Internal Dispatch Decision.py`
- `ApexBEMS -Market API.py`

Despite the `.py` extension, these files are JSON Schema documents. The tests validate representative example payloads against them.

## Public Benchmark vs Site Proof

The public benchmark can be run immediately:

```powershell
.\.venv\Scripts\python.exe scripts\run_public_benchmark.py --node hbHubAvg --market rt --horizon-steps 8 --miner-power-kw 1000 --miner-efficiency-j-per-th 25
```

It writes:

```text
reports/public_benchmark_rt_hbHubAvg.md
reports/public_benchmark_rt_hbHubAvg.json
reports/public_benchmark_rt_hbHubAvg_dispatch.csv
```

This proves ApexBEMS optimizer behavior against real public market and Bitcoin network conditions. It does not prove readiness to write commands to a private site. The next proof layer is read-only shadow mode using the facility's actual miner telemetry, PCS telemetry, transformer and breaker limits, tariff terms, control history, alarms, and curtailment events.

Important unit boundary: public ERCOT prices are reported in `$/MWh` and converted to optimizer `$/kWh` before dispatch optimization. The benchmark and tests verify this conversion and allow negative ERCOT prices.

## Step 1: Expose Mining Load Control

The future optimizer needs one controllable variable from the mining site:

```text
P_MINE(t) = site mining power in kW
```

Possible control sources:

- Foreman API.
- LuxOS RPC.
- Custom miner manager RPC.
- ASIC frequency/voltage groups.
- Site-level contactor or breaker controls for emergency or coarse curtailment only.

Target dry-run command shape:

```json
{
  "timestamp": "2026-01-01T12:00:00Z",
  "site_id": "site-a",
  "command_id": "miner-1",
  "target_power_kw": 900.0,
  "ramp_seconds": 60,
  "reason": "price-responsive curtailment"
}
```

This command should be generated and signed in dry-run mode before any live miner-manager integration is enabled.

## Step 2: Add Mining Economics to Optimization

The current optimizer does not include `P_MINE[t]`. To integrate mining properly, add:

```text
P_MINE[t] in [P_MINE_MIN, P_MINE_MAX]
```

Then extend site power balance:

```text
Sign convention:
- P_GRID_IMPORT[t] > 0 means importing from the grid.
- P_BATT[t] > 0 means the battery is discharging/exporting to the site or grid.
- P_BATT[t] < 0 means the battery is charging/importing.

P_GRID_IMPORT[t] =
    P_MINE[t]
  + other_site_load[t]
  - onsite_generation[t]
  - P_BATT[t]
```

Mining value can be represented as marginal value in `$/kWh`:

```text
mining_value_per_kwh =
    expected_btc_revenue_per_kwh
  + expected_fee_revenue_per_kwh
  - marginal_operating_cost_per_kwh
```

This value depends on miner efficiency, BTC price, block subsidy, transaction fees, network hashrate, pool fees, uptime, and site-specific operating costs.

The objective should include:

```text
market_revenue
+ mining_value
- battery_degradation
- imbalance_penalties
- curtailment_penalties
```

## Step 3: Wire Miner Commands Through EventBus

Initial dry-run pattern:

```python
event_type = "dispatch_decision"
callback = write_signed_miner_dry_run_command
```

The callback should translate the optimized mining setpoint into a signed dry-run artifact first. Live miner-manager instructions are a later staged-control phase after replay validation, operator approval, asset-specific safety checks, and hardware-in-the-loop testing.

Hard requirements:

- Idempotent commands using `command_id`.
- Rate limits and ramp limits.
- Fail-closed behavior on stale telemetry.
- Manual override support.
- Audit log entry for every issued command.
- Signed dry-run output before live dispatch.
- Asset-specific miner safety gateway and schema validation before command emission.

## Step 4: Wire Battery PCS Commands

Target PCS command shape:

```json
{
  "timestamp": "2026-01-01T12:00:00Z",
  "site_id": "site-a",
  "command_id": "pcs-1",
  "setpoint_kw": -125.0,
  "ramp_seconds": 30,
  "reason": "charge before high-price interval"
}
```

Implementation targets:

- Modbus TCP.
- SunSpec.
- CAN-to-TCP gateway.
- Vendor REST API.

Before live control, implement a dry-run PCS adapter that validates schemas, signs command artifacts, and writes commands to the audit log.

Hard requirements:

- Stale telemetry lockout.
- Manual override lockout.
- PCS availability and alarm checks.
- Ramp-rate and power-limit checks.
- Asset-specific PCS safety gateway before command emission.

## Step 5: Normalize Telemetry

Telemetry should arrive in the unified site envelope:

```json
{
  "timestamp": "2026-01-01T12:00:00Z",
  "site_id": "site-a",
  "streams": {
    "miner": {},
    "pcs": {},
    "market": {},
    "btc": {}
  }
}
```

Adapter responsibilities:

- Validate schema.
- Preserve missing safety fields as missing; do not invent them during replay or parsing.
- Reject stale timestamps.
- Convert market feed into the current `market_data` DataFrame with a `price` column.
- Convert PCS telemetry into battery SOC, power, and temperature updates.
- Convert mining telemetry into `P_MINE` availability and economic inputs.
- Capture breaker, transformer, tariff, alarm, and override state for shadow-mode evidence.
- Capture transformer capacity, interconnection limit, and curtailment agreement state.

## Step 6: Connect Market Submission

The current `MarketAPIClient` is simulated. Market submission is blocked by default in shadow mode. Any future production integration should wrap real market APIs while keeping the same internal contract and requiring explicit configuration.

Target bid payload:

```json
{
  "timestamp": "2026-01-01T12:00:00Z",
  "site_id": "site-a",
  "market": "ERCOT",
  "product": "energy",
  "interval_start": "2026-01-01T12:05:00Z",
  "bid_curve": [
    {"price": 45.0, "quantity_kw": 250.0}
  ]
}
```

Every bid should pass through `PolicyValidator` before submission.
Every battery dispatch should pass through the current `SafetyGateway` before state update. Future miner, PCS, and site-level commands should add asset-specific safety gateways before any dry-run or live command output.

## Step 7: Shadow-Mode Site Proof

Before any staged activation, run a site-specific shadow-mode campaign:

- Collect at least 30 days of PCS, meter, miner, breaker, alarm, tariff, and market data.
- Replay decisions against that fixture set.
- Record signed dry-run PCS and miner commands.
- Compare recommendations to actual operator/site behavior.
- Report optimizer success/failure, safe fallback, SOC clipping, raw SOC violations, curtailment opportunities, missed revenue, and override reasons.
- Review replayable audit logs with the operator.

## Implementation Checklist

- [x] Add schema loader and validator helpers.
- [ ] Add contract adapters for telemetry, dispatch decisions, PCS commands, miner commands, and bids.
- [ ] Add `site_id` to runtime configuration.
- [ ] Add `dispatch_id` and `command_id` generation.
- [ ] Add `P_MINE[t]` to the optimizer.
- [ ] Add mining economics to the objective.
- [ ] Add signed miner manager dry-run adapter.
- [ ] Add signed PCS dry-run adapter.
- [ ] Add market dry-run adapter for ISO bid payloads.
- [ ] Add per-asset safety gateways for miner, PCS, site interconnection, and market command outputs.
- [ ] Add tests for all adapters.
- [ ] Run live integrations only behind explicit configuration flags.
- [ ] Run 30-day site telemetry replay before staged activation.
