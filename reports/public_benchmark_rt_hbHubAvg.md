# ApexBEMS Public Telemetry Replay Benchmark

Generated UTC: `2026-06-25T04:51:01.500838+00:00`
Source: `ERCOT dashboard RT SPP (https://www.ercot.com/api/1/services/read/dashboards/system-wide-prices.json)`
Site ID: `public-benchmark`
Market/node/product: `ERCOT` / `hbHubAvg` / `energy`
Data window: `2026-06-24T05:15:00+00:00` to `2026-06-25T04:30:00+00:00`
Dispatch interval: `15.0 minutes`
Horizon/scenarios/seed: `8` / `3` / `7`

## Reproducibility

- Original live run command: `python.exe scripts/run_public_benchmark.py --node hbHubAvg --market rt --horizon-steps 8 --out-dir reports`
- Reproduction from saved JSON: `python.exe scripts/run_public_benchmark.py --node hbHubAvg --market rt --horizon-steps 8 --out-dir reports`
- Regenerated from JSON: `False`
- Source JSON: `not applicable`
- Git commit: `2c4dcdbe2ca95da65540b8a3e1b9c1d4ef4d4149`
- Git dirty: `True`
- Python: `3.13.7 (tags/v3.13.7:bcee1c3, Aug 14 2025, 14:15:11) [MSC v.1944 64 bit (AMD64)]`
- Platform: `Windows-11-10.0.26200-SP0`
- Package versions: `PuLP=3.3.2, jsonschema=4.26.0, numpy=2.4.6, pandas=3.0.3, prophet=1.3.0, pytest=9.0.2, scikit-learn=1.9.0, scipy=1.18.0, shap=0.52.0, tensorflow=not-installed, xgboost=3.3.0`

## Data Provenance

- ERCOT prices: `https://www.ercot.com/api/1/services/read/dashboards/system-wide-prices.json`
- BTC spot: `https://api.coinbase.com/v2/prices/BTC-USD/spot`
- Bitcoin fees: `https://mempool.space/api/v1/fees/recommended`
- Bitcoin hashrate: `https://mempool.space/api/v1/mining/hashrate/3d`
- Recent blocks: `https://mempool.space/api/v1/blocks`

## Data Quality Scorecard

- Score / grade: `1.0` / `A`
- Gate Status: `Pass`
- Headline Claimability: `Eligible for full public-data benchmark claim`
- Evidence level: `full_public_data_evidence`
- Claimable for headline KPI: `True`
- Source tier: `tier_a_official_public`
- Fallback used: `False`
- Market data age: `21.025` minutes
- Market fetch age: `0.215` minutes
- BTC fetch age: `0.203` minutes
- Market fetch timestamp: `2026-06-25T04:50:48.605861+00:00`
- BTC fetch timestamp: `2026-06-25T04:50:49.298698+00:00`
- Completeness ratio: `1.0`
- Completeness score: `1.0`
- ERCOT provider disagreement: `False`
- BTC provider disagreement: `False`
- ERCOT price relative delta: `0.0`
- BTC spot relative delta: `0.0009141549403675587`
- Reason(s): `none`
- Gate status:
  source_tier_known=`True`, fallback_clear=`True`, market_data_fresh=`True`, market_fetch_timestamp_present=`True`, btc_fetch_timestamp_present=`True`, market_fetch_fresh=`True`, btc_fetch_fresh=`True`, completeness=`True`, btc_metadata_present=`True`, ercot_providers_agree=`True`, btc_providers_agree=`True`, unit_consistency_enforced=`True`, shadow_safety_mode=`True`

## Reconciliation Panel

- ERCOT primary/secondary: `ercot_dashboard_primary` / `ercot_dashboard_secondary`
- ERCOT overlap intervals: `94`
- ERCOT max relative delta: `0.0`
- ERCOT delta threshold: `0.05`
- ERCOT disagreement: `False`
- BTC primary/secondary: `coinbase` / `coingecko`
- BTC primary/secondary USD: `60990.755` / `60935.0`
- BTC relative delta: `0.0009141549403675587`
- BTC delta threshold: `0.02`
- BTC disagreement: `False`
- Failed quality gates: `none`

## Telemetry Replay Layer

- Telemetry snapshots generated: `94`
- First snapshot hash: `c721190babf582be65b74145479a4f8831c5c0c0b77388fc294448c1ec35a5c8`
- Last snapshot hash: `ffe6e1f2383996f35802f4da5a9342a665d32cee4fdd1a063f3a8b4337cefb9b`
- Snapshot fields include market price, normalized optimizer price, battery SOC/temp/health, mining proxy inputs, and quality flags.
- Public replay snapshots intentionally mark private breaker, alarm, transformer, and operator override fields as unavailable.

## Storage Dispatch Results

- Intervals tested: `94`
- Optimizer success rate: `100.00%`
- Optimizer successes: `94`
- Optimizer failures: `0`
- Safe fallback intervals: `0`
- SOC violations before clipping: `0`
- SOC clipping events: `0`
- Final SOC: `0.2355`
- Price range: `$18.70` to `$51.09`/MWh
- Total storage revenue vs hold: `$15.15`
- Throughput: `1841.10` kWh
- Charge / discharge / idle intervals: `17` / `22` / `55`
- Solver/time limit: `CBC` / `10` seconds
- Battery limits: `1000 kWh, 250 kW, SOC 10%-90%`
- Safety flags: `shadow_mode=True, allow_market_submission=False, dry_run_commands_only=True`

Storage revenue is calculated for the configured reference asset: 1000 kWh capacity, 250 kW max power, 15.0 minutes dispatch interval, and the benchmark data window. It is not annualized and is not a site revenue forecast.

## Mining Proxy

- BTC spot: `$60990.75`
- Network hashrate: `959.51` EH/s
- Average recent block fees: `0.01473` BTC
- Assumed miner load: `1000` kW
- Assumed miner efficiency: `25.0` J/TH
- Gross revenue: `$28.74` per PH/day
- Estimated break-even power price: `$47.90`/MWh
- Estimated always-on mining power-cost margin over benchmark window: `$458.86`
- Curtailment candidate intervals: `2`

This is a proxy based on BTC spot, network hashrate, recent fees, miner efficiency, assumed load, and benchmark power prices. It does not include pool fees, downtime, curtailment contracts, hosting fees, firmware behavior, or miner fleet telemetry.

## What This Proves / Does Not Prove

This benchmark proves:

- ERCOT public price ingestion and explicit USD/MWh to USD/kWh conversion.
- Optimizer execution across real public price intervals.
- SOC safety accounting before clipping.
- Telemetry-style replay snapshot generation.
- Stable snapshot and decision hashes for audit/replay.
- Mining break-even proxy calculation.

This benchmark does not prove:

- Private site control readiness.
- PCS or miner command safety.
- Breaker, transformer, or tariff compliance.
- SCADA integration.
- Live ISO bidding readiness.
- Real miner fleet telemetry behavior.

## Interpretation

This is a public-data telemetry replay benchmark against real market and Bitcoin network signals. It proves optimizer behavior on public conditions, not direct control readiness for a private site. Production readiness still requires read-only shadow mode against private PCS, miner, breaker, meter, transformer, and SCADA telemetry.

## Audit Notes

- `reports/*_dispatch.csv` should contain interval price, dispatch, SOC, solver status, revenue, snapshot hash, and decision hash fields.
- `reports/*_telemetry.csv` should contain replay telemetry snapshots.
- `reports/*.json` should contain the full machine-readable summary, assumptions, data-source URLs, telemetry, and dispatch records.
- Public market data cannot verify private alarms, curtailment agreements, breaker limits, transformer limits, or miner uptime.
