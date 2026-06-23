# ApexBEMS v7.0 Verified Implementation Analysis

This document describes what the current repository implements today, what is only represented as an integration contract, and what must be protected during future refactors. It reflects the current verified state after the modular split, public benchmark hardening, safety gateway, schema validation, metrics, and replayable audit updates.

## Current Repository Shape

ApexBEMS is now a preserved legacy monolith plus a modular implementation package:

- `ApexBEMS.py`: preserved legacy monolith containing configuration, event bus, battery state, forecasting wrappers, stochastic optimization, audit logging, market API simulation, controller orchestration, and demo entry point.
- `apex_bems/`: modular package with the current implementation target for configuration, forecasting, optimization, safety, audit, benchmark, metrics, schema validation, controller orchestration, and market simulation.
- `schemas/`: JSON Schema contract documents stored with `.py` extensions.
- `tests/`: pytest safety net covering configuration, battery state, event bus behavior, audit logging, feature engineering, optimizer execution, controller stepping, schema validity, real-world scenarios, public benchmark mechanics, production hardening, modular safety checks, and legacy-vs-modular parity.
- `reports/`: generated public-data benchmark outputs from live ERCOT and Bitcoin network feeds.
- `requirements.txt`: runtime and test dependencies.

The monolith remains functional and tested. New development should target the modular `apex_bems` package while legacy imports from `ApexBEMS.py` remain supported.

## Verified Status

The current repository is best described as:

> ApexBEMS is a test-covered, public-data benchmarked, shadow-mode energy optimization engine with safety-gated dispatch recommendations and replayable audit logs.

Verified local test status:

- Pytest: `79 passed`.
- Public benchmark: `66` ERCOT `hbHubAvg` real-time intervals replayed.
- Optimizer success rate: `100.00%`.
- Optimizer failures: `0`.
- Safe fallback intervals: `0`.
- SOC violations before clipping: `0`.
- SOC clipping events: `0`.
- Safety gateway: enabled.
- Shadow mode: default behavior.
- Market submission: blocked by default unless explicitly enabled.

This is strong evidence for shadow-mode pilot readiness. It is not evidence of autonomous production control against a live mining facility.

## Verified Capabilities

The current implementation has automated coverage for:

- `BEMSConfig` validation.
- `BatteryStateService` update, clipping, health estimate, and persistence round trip.
- `EventBus` sync and async subscriber dispatch.
- `AuditLogger` SQLite writes and bottleneck aggregation.
- Price feature engineering through `prepare_price_features`.
- Real PuLP optimization on a minimal stochastic market problem.
- Bid curve generation and SOC restoration.
- Policy validation rejection for over-committed bids.
- `MPController.step` with stubbed forecasts and real audit/state outputs.
- Negative-price dispatch solving without unbounded imbalance rewards.
- Correct controller SOC direction for charge vs discharge.
- Multi-step volatile operating-day simulation with audit verification.
- Public-data benchmark harness that replays live ERCOT dashboard prices through the implemented optimizer and computes Bitcoin mining break-even proxies from public network data.
- Modular safety checks for SOC bounds, solver/product validation, raw SOC violation detection before clipping, segment-based degradation constraints, price-unit rejection, input-shape validation, safe fallback metadata, physical dispatch linkage, finite dispatch values, and blocked market submission.
- Audit-grade parity tests comparing `ApexBEMS.py` and `apex_bems` outputs for config, policy, features, forecasting fallbacks, optimizer results, bid curves, market simulation, controller state, and audit rows.
- JSON Schema validity for all schema documents.
- Example payload validation for the external contract schemas.
- Replayable audit context and deterministic JSON hashing for benchmark and decision evidence.
- Negative ERCOT prices and price spikes in parser and benchmark tests.
- Mining break-even unit correctness.

Run:

```powershell
.\.venv\Scripts\python.exe -m pytest -v
```

Expected result:

```text
79 passed
```

Run the live public benchmark:

```powershell
.\.venv\Scripts\python.exe scripts\run_public_benchmark.py --node hbHubAvg --market rt --horizon-steps 8 --miner-power-kw 1000 --miner-efficiency-j-per-th 25
```

The benchmark writes Markdown, JSON, and CSV artifacts under `reports/`. It validates behavior on real public prices and Bitcoin network signals, but it does not replace read-only shadow mode against private site telemetry.

## Implemented Architecture

The current internal flow is:

```text
Market/BTC/Telemetry inputs
        |
        v
SchemaValidation + Price Unit Checks
        |
        v
MPController.step()
        |
        +--> ForecasterService.get_price_scenarios()
        +--> OptimizationService.generate_bid_curve()
        +--> PolicyValidator.validate_bid()
        +--> OptimizationService.optimize()
        +--> SafetyGateway.validate_dispatch()
        +--> BatteryStateService.update_state()
        +--> AuditLogger.log_plan()
        +--> MetricsRegistry.snapshot()
        +--> MarketAPIClient.submit_bid()
             only when shadow_mode=False and allow_market_submission=True
```

The runtime input accepted by `MPController.step()` is currently a Pandas DataFrame with a `price` column. Public benchmark and schema tests validate external payload shapes, but a full live site telemetry adapter is still a future phase.

## Safety, Auditability, and Shadow Mode

The current modular implementation includes production-hardening primitives intended to make recommendations auditable before any real control integration:

- `SafetyGateway` validates finite dispatch, configured power limits, raw SOC movement before clipping, clipped SOC, and violation metadata.
- `PolicyValidator` rejects unsafe or over-committed bid decisions.
- `BEMSConfig` defaults to shadow mode and blocks market submission by default.
- `AuditLogger` records dispatch plans, safety fields, decision context, stable hashes, and replayable records.
- `MetricsRegistry` tracks optimizer success/failure, safe fallback, SOC clipping, and SOC violation counters.
- `schema_validation.py` validates contract payloads without inventing missing safety fields.
- Public benchmark code converts ERCOT `$/MWh` market prices to optimizer `$/kWh` inputs and rejects wrong optimizer price units.

## Contract-Only Surfaces

The schema folder defines external contracts that are not fully wired into the monolith yet:

- Miner telemetry.
- PCS/battery telemetry.
- Market price and forecast feeds.
- BTC and fee market feed.
- Unified site telemetry envelope.
- Miner control command.
- PCS command.
- Internal dispatch decision payload.
- ISO bid payload.

The current code emits internal objects such as `DispatchPlan` and `List[Tuple[price, quantity_kw]]`. Schema validation exists, but full live adapters for site telemetry, signed dry-run command payloads, PCS command output, miner control output, and ISO bid submission remain future implementation work.

## Important Implementation Gaps

These should be addressed before calling the system production-ready:

- Live site telemetry adapters are missing. Add read-only adapters for PCS, meter, miner, breaker, tariff, and SCADA/event streams.
- Signed dry-run command output is missing. Add command signing and replayable dry-run artifacts before any real control path.
- Miner load is not yet an optimizer decision variable. Current optimization controls battery/market commitments, not `P_MINE[t]`.
- PCS and miner control integrations are not implemented. Current market API remains simulated and blocked by default in shadow mode.
- Public benchmark data is not private site telemetry. It cannot prove behavior against a specific mining facility's PCS alarms, miner uptime, breaker limits, tariff details, or SCADA control path.
- README and older strategy docs previously referenced thermal derating. Current code tracks temperature for degradation cost but does not implement hard thermal cutoffs or derating constraints.
- The schema files use `.py` extensions. They parse as JSON and Python literals, but should eventually be renamed to `.schema.json` or moved behind a schema loader.

## Refactor Status and Priorities

The first split-only refactor introduced the following modular structure:

1. `config.py`: `BEMSConfig` and constants.
2. `events.py`: `EventBus`.
3. `battery.py`: `BatteryStateService`.
4. `audit.py`: `AuditLogger`.
5. `forecasting.py`: feature engineering and forecaster classes.
6. `optimization.py`: solver factory and `OptimizationService`.
7. `market.py`: `MarketAPIClient`.
8. `controller.py`: `MPController`, `DispatchPlan`, `main_services`.
9. `safety.py`: `SafetyGateway` and safety validation results.
10. `metrics.py`: in-memory metrics counters and snapshots.
11. `schema_validation.py`: JSON Schema loading and validation helpers.
12. `benchmark.py`: public-data benchmark execution and replay support.

Full live adapter modules remain a future phase.

Refactor rule: keep `ApexBEMS.py` as the legacy baseline and add behavior changes only after both legacy and modular tests remain green.

## Testing Standard

Every new integration should add tests in the same style:

- Unit tests for validation and edge cases.
- Contract tests against JSON Schema payloads.
- Integration smoke tests with temp files and stubbed network calls.
- No real market, miner, PCS, or cloud calls in default test runs.

## Validation Boundary

Current evidence supports a shadow-mode pilot claim. It does not support calling ApexBEMS a production autonomous controller.

The next milestone should be a 30-day replay benchmark using fixture data, a read-only shadow-mode telemetry adapter for PCS, meter, and miner streams, and signed dry-run command output. That is the difference between a strong public repository and a pilot-ready deployment package for an operator.
