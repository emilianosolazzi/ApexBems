# ApexBEMS Public Real-World Benchmark

Generated UTC: `2026-06-22T21:48:55.796626+00:00`
Source: `ERCOT dashboard RT SPP (https://www.ercot.com/api/1/services/read/dashboards/system-wide-prices.json)`
Node: `hbHubAvg`
Data window: `2026-06-22T05:15:00+00:00` to `2026-06-22T21:30:00+00:00`
Dispatch interval: `15.0 minutes`
Horizon/scenarios/seed: `8` / `3` / `7`

## Reproducibility

- Original live run command: `python.exe scripts\run_public_benchmark.py --node hbHubAvg --market rt --horizon-steps 8 --miner-power-kw 1000.0 --miner-efficiency-j-per-th 25.0`
- Reproduction from saved JSON: `python.exe scripts\run_public_benchmark.py --from-json reports\public_benchmark_rt_hbHubAvg.json`
- Regenerated from JSON: `True`
- Source JSON: `F:\ApexBems-main(1)\ApexBems-main\reports\public_benchmark_rt_hbHubAvg.json`
- Git commit: `e81034ab97bfb7bceeb92460289c079b17209c55`
- Git dirty: `False`
- Python: `3.12.13 (main, May 10 2026, 19:35:37) [MSC v.1944 64 bit (AMD64)]`
- Platform: `Windows-11-10.0.26200-SP0`
- Package versions: `PuLP=3.3.2, jsonschema=4.26.0, numpy=2.4.6, pandas=3.0.3, prophet=1.3.0, pytest=9.1.1, scikit-learn=1.9.0, scipy=1.18.0, shap=0.52.0, tensorflow=2.21.0, xgboost=3.3.0`

## Data Provenance

- ERCOT prices: `https://www.ercot.com/api/1/services/read/dashboards/system-wide-prices.json`
- BTC spot: `https://api.coinbase.com/v2/prices/BTC-USD/spot`
- Bitcoin fees: `https://mempool.space/api/v1/fees/recommended`
- Bitcoin hashrate: `https://mempool.space/api/v1/mining/hashrate/3d`
- Recent blocks: `https://mempool.space/api/v1/blocks`

## Storage Dispatch Results

- Intervals tested: `66`
- Optimizer success rate: `100.00%`
- Optimizer failures: `0`
- Safe fallback intervals: `0`
- SOC violations before clipping: `0`
- SOC violations before clipping inferred: `False`
- SOC clipping events: `0`
- SOC clipping events inferred: `False`
- Final SOC: `0.2822`
- Price range: `$19.67` to `$46.86`/MWh
- Total storage revenue vs hold: `$9.47`
- Throughput: `1230.52` kWh
- Charge / discharge / idle intervals: `14` / `19` / `33`
- Solver/time limit: `CBC` / `30` seconds
- Battery limits: `1000 kWh, 250 kW, SOC 10%-90%`
- Safety flags: `physical_dispatch_link=True, enforce_price_unit_check=True`

Storage revenue is calculated for the configured reference asset: 1000 kWh capacity, 250 kW max power, 15.0 minutes dispatch interval, and the benchmark data window. It is not annualized and is not a site revenue forecast.

## Mining Proxy

- BTC spot: `$64176.12`
- Network hashrate: `941.82` EH/s
- Average recent block fees: `0.01405` BTC
- Assumed miner load: `1000` kW
- Assumed miner efficiency: `25.0` J/TH
- Gross revenue: `$30.80` per PH/day
- Estimated break-even power price: `$51.34`/MWh
- Estimated always-on mining power-cost margin over benchmark window: `$410.34`
- Curtailment candidate intervals: `0`

This is a proxy based on BTC spot, network hashrate, recent fees, miner efficiency, assumed load, and benchmark power prices. It does not include pool fees, downtime, curtailment contracts, hosting fees, firmware behavior, or miner fleet telemetry.

## What This Proves / Does Not Prove

This benchmark proves:

- ERCOT public price ingestion and unit conversion.
- Optimizer execution across real public price intervals.
- SOC safety accounting before clipping.
- Benchmark audit artifact generation.
- Mining break-even proxy calculation.

This benchmark does not prove:

- Private site control readiness.
- PCS or miner command safety.
- Breaker, transformer, or tariff compliance.
- SCADA integration.
- Live ISO bidding readiness.

## Interpretation

This is a public-data benchmark against real market and Bitcoin network signals. It proves optimizer behavior on public conditions, not direct control readiness for a private site. Production readiness still requires read-only shadow mode against site PCS, miner, breaker, and SCADA telemetry.

## Audit Notes

- `reports/*_dispatch.csv` contains interval-by-interval price, dispatch, SOC, solver status, and revenue fields.
- `reports/*.json` contains the full machine-readable summary, assumptions, data-source URLs, and dispatch records.
- Public market data cannot verify private alarms, curtailment agreements, breaker limits, transformer limits, or miner uptime.
