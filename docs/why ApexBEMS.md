# Why ApexBEMS

ApexBEMS is a safety-gated shadow-mode energy-market optimization engine built around forecast-aware dispatch, stochastic optimization, explicit degradation economics, and auditability.

This document explains the system in operator terms while staying aligned with the current verified repository. New development should use the modular `apex_bems` package; `ApexBEMS.py` remains as a preserved legacy monolith.

Current verified claim:

> ApexBEMS is a test-covered, public-data benchmarked, shadow-mode energy optimization engine with safety-gated dispatch recommendations and replayable audit logs.

Current validation snapshot:

- Pytest: `79 passed`.
- Public benchmark: `66` ERCOT `hbHubAvg` real-time intervals.
- Optimizer success rate: `100.00%`.
- Optimizer failures: `0`.
- Safe fallback intervals: `0`.
- SOC violations before clipping: `0`.
- Market submission: blocked by default.

## 1. Forecasting Ensemble

ApexBEMS can combine multiple forecasting approaches:

- LSTM neural networks when TensorFlow is installed.
- Prophet for trend and seasonality.
- XGBoost for short-horizon tree-based regression.

The `EnsembleForecaster` tracks model regret and adjusts weights toward models with lower recent error. If optional forecasting models are unavailable or untrained, the system falls back to a naive last-price forecast rather than failing the dispatch loop.

Current implementation:

- Feature engineering is implemented in `prepare_price_features`.
- LSTM, Prophet, and XGBoost wrappers exist.
- VAE scenario generation exists with a Gaussian fallback when untrained.
- Default tests avoid long model training and instead verify feature generation and controller integration with stubbed scenarios.

## 2. MPC Optimization Engine

ApexBEMS uses model predictive control: each step optimizes over a look-ahead horizon, executes the first action, then repeats as new market data arrives.

The optimizer currently models:

- Day-ahead power commitment.
- Real-time deviations by scenario.
- SOC constraints.
- Reserve products: regulation up, regulation down, and spinning reserve.
- Imbalance penalties.
- Piecewise battery degradation cost.
- Terminal SOC slack.

Current implementation:

- The LP is built in `OptimizationService`.
- PuLP is used as the solver interface.
- CBC is the default fallback solver.
- Minimal optimizer execution, negative-price boundedness, volatile-day controller behavior, and legacy-vs-modular parity are covered by pytest.
- SOC dynamics use efficiency-aware charge and discharge terms.

## 3. Battery Degradation Accounting

ApexBEMS prices battery wear inside the optimization objective using piecewise degradation costs.

Current implementation:

- `BatteryStateService` tracks SOC, temperature, cycle count, and calendar days.
- Arrhenius-style temperature factor is used in degradation cost calculations.
- State is persisted through `battery_state.json`.
- Corrupt state files are renamed with `.corrupt` and defaults are used.

Not yet implemented:

- Hard thermal cutoff.
- Thermal derating constraints.
- PCS telemetry ingestion from the schema envelope.

## 4. Explainability and Audit Trail

ApexBEMS is designed to be auditable before it becomes autonomous. The current implementation defaults to shadow-mode recommendations and blocks market submission unless explicitly configured.

Each dispatch decision can be written to SQLite through `AuditLogger`. Logged values include:

- Timestamp.
- Action in kW.
- Reason string.
- Shadow prices.
- Top model features when SHAP is available.
- Bid curve.
- SOC.
- Temperature.
- Cycle count.
- Safety fields.
- Stable decision-context hash.

The current test suite verifies SQLite audit writes, bottleneck aggregation, replayable decision context, stable JSON hashes, safety fields, and legacy-vs-modular audit-row parity.

Default runtime files:

```text
audit_log.db
battery_state.json
```

These are runtime artifacts and are ignored by `.gitignore`.

## 5. Schema-First Integration Target

The `schemas/` folder defines the target external contracts for site telemetry, miner control, PCS commands, dispatch decisions, and ISO bid payloads.

Current status:

- Schema documents are valid draft 2020-12 JSON Schema.
- Example payloads validate in tests.
- Modular schema validation helpers exist.
- The monolith does not yet parse or emit those schemas directly.

Next implementation target:

- Add a read-only shadow-mode telemetry adapter for PCS, meter, miner, breaker, tariff, and alarm streams.
- Add signed dry-run command output for PCS/miner recommendations.
- Run a 30-day replay benchmark using fixture data before any staged control activation.
