# ApexBEMS vs. Existing Platforms

ApexBEMS is best understood as an open, auditable, safety-gated shadow-mode optimization engine for storage and flexible energy assets. The current repository includes a preserved Python monolith, a modular `apex_bems` package, schema contracts, read-only telemetry normalization, replayable public-data benchmarks, a read-only shadow-site runner, and an 87-test safety/parity suite; it is not yet a complete commercial SCADA/ISO integration product or live-control deployment package.

This comparison is not claiming that ApexBEMS currently replaces mature commercial EMS, SCADA, or VPP products. Many commercial systems already include field-tested integrations, market interfaces, support teams, and operational certifications. ApexBEMS differentiates on openness, auditability, reproducibility, safety-gated shadow mode, and inspectable optimization logic.

Current verified claim:

> ApexBEMS includes a virtual-site HIL simulator that proves command contracts, safety gating, adapter acknowledgements, telemetry feedback, and audit persistence using real benchmark-seeded conditions before live hardware integration.

## Capability Matrix

| Capability | Current ApexBEMS Repository | Typical Commercial EMS / VPP Platform |
|---|---|---|
| Optimization core | Stochastic LP/MPC-style dispatch with PuLP | Usually proprietary |
| Battery degradation | Piecewise degradation costs with temperature factor | Often proprietary or vendor-specific |
| Forecasting | LSTM, Prophet, XGBoost wrappers plus fallbacks | Proprietary or external |
| Explainability | Shadow prices and optional SHAP feature importance | Often limited |
| Audit trail | SQLite dispatch log with replayable decision context | Platform-specific |
| Safety controls | `SafetyGateway`, `PolicyValidator`, read-only telemetry adapters, shadow-mode defaults, blocked market submission | Vendor-specific or hidden |
| Metrics | Optimizer success/failure, safe fallback, SOC clipping, SOC violation counters | Often proprietary or vendor-specific |
| Schema contracts | JSON Schema documents plus validation helpers | Vendor-specific APIs |
| Public benchmark | ERCOT `$/MWh` to optimizer `$/kWh` replay with Bitcoin mining proxy | Usually internal or unavailable |
| Source access | Preserved monolith plus modular package | Closed |
| Testability | Pytest suite with production-hardening, benchmark, real-world, and parity coverage | Usually not externally inspectable |
| Miner/PCS connectors | Read-only mapping/replay telemetry adapter plus contracts; no live vendor driver | Vendor-dependent |
| ISO integrations | Simulated client only, market submission blocked by default | Usually available in commercial platforms |

## Current Strengths

### Open Optimization Core

The optimization model is visible and testable. Engineers can inspect constraints, objective terms, solver configuration, and dispatch outputs.

### Auditability

Dispatch decisions can be written to SQLite with reason strings, shadow prices, bid curves, safety fields, stable hashes, and state metrics. This is a strong foundation for compliance, replay, and post-event review.

### Refactor-Friendly Test Baseline

The test suite covers core behavior, production-hardening checks, public benchmark mechanics, real-world dispatch scenarios, and parity between the preserved monolith and the modular package.

### Safety-Gated Shadow Mode

The modular controller defaults to recommendation-only behavior. Dispatch is checked by `SafetyGateway` before state update or submission, telemetry is normalized through a read-only adapter layer, and market submission is blocked unless explicitly enabled.

### Public Benchmark Evidence

The benchmark replays public ERCOT real-time prices through the optimizer, converts market prices from `$/MWh` to `$/kWh`, and reports machine-readable JSON, Markdown, and CSV artifacts. The refreshed `hbHubAvg` benchmark covers 66 intervals with 100% optimizer success, zero optimizer failures, zero safe fallback intervals, and zero raw SOC violations before clipping.

## Virtual-Site HIL Proof

The repository now includes a virtual-site HIL simulator and proof artifact.

- HIL status: PASS
- PCS command: accepted
- Miner command: accepted
- Safety gate: passed
- Telemetry feedback: updated
- Audit persistence: confirmed
- Artifact: `reports/virtual_site_hil_latest.json`

### Schema-First Direction

The repository contains explicit contract documents for telemetry and command payloads. These contracts now have tests that validate representative examples, including PCS ramp/mode fields, breaker state, transformer state, feeder constraints, and site telemetry envelope references.

## Where ApexBEMS Is Strongest Today

ApexBEMS is strongest as a transparent shadow-mode decision engine for:

- Battery storage dispatch analysis.
- ERCOT/public-data benchmark replay.
- Safety-gated recommendation workflows.
- Engineering teams that need inspectable optimization logic.
- Pilot studies where no control writes are allowed.
- Sites evaluating storage plus flexible-load economics before live control integration.

It is especially useful when the buyer needs to understand why a dispatch recommendation was made, what constraints were binding, whether SOC safety was preserved, and whether the decision can be replayed later.

## Why It Matters

Energy assets are becoming more controllable, but most operators still face the same problem: they need better dispatch decisions without giving unproven software direct control over equipment.

ApexBEMS is designed around that adoption reality.

Instead of starting with live control, ApexBEMS starts with shadow-mode recommendations:

- Read market and site data.
- Generate dispatch recommendations.
- Validate each recommendation against safety limits.
- Log the full decision context.
- Compare recommendations against actual site behavior.
- Prove value before enabling command writes.

This makes ApexBEMS useful before any production control path is considered. Operators can evaluate whether the optimizer improves economics, preserves SOC safety, respects constraints, and produces replayable evidence without risking live equipment.

## Shadow Mode First

The current repository defaults to shadow mode. Market submission is disabled unless explicitly enabled, and hardware command writes are not part of the current live path.

That design choice is intentional.

For batteries, miners, EV chargers, data centers, and industrial loads, the safest first deployment is not live automation. The safest first deployment is a read-only replay or shadow-mode pilot where ApexBEMS produces recommendations and audit logs while the site continues operating normally.

A successful shadow-mode pilot should answer:

- What would ApexBEMS have recommended?
- Was the recommendation safe?
- Was SOC preserved within limits?
- Did the optimizer fail or fall back?
- Would the recommendation have improved economics?
- Can the decision be replayed and explained later?

## Pilot Proof Target

The next commercial proof point is a 30-day shadow-mode replay against real site telemetry.

Target pilot output:

- Actual site behavior vs. ApexBEMS recommended behavior.
- Estimated dispatch value difference.
- SOC safety result.
- Unsafe recommendation count.
- Safe fallback count.
- Optimizer failure count.
- Curtailment or flexible-load opportunity windows.
- Replayable audit trail with stable decision hashes.

The key proof sentence should become:

> ApexBEMS replayed 30 days of real site telemetry and found measurable dispatch value with zero unsafe recommendations.

That is the bridge from public benchmark evidence to operator-grade pilot evidence.

## Current Limitations

These are implementation gaps, not positioning details:

- No live ISO market connector.
- No live PCS driver or SCADA control path.
- No live miner manager connector.
- No live vendor telemetry drivers for private site meter, PCS, breaker, transformer, feeder, tariff, alarm, and miner streams. Read-only mapping/replay normalization is implemented.
- No cryptographic signatures on dry-run command artifacts yet.
- Mining load is not yet part of the optimizer decision variables.
- Battery thermal derating is not implemented, despite temperature being tracked for degradation. Transformer thermal limit blocking is implemented when telemetry is provided.
- The schema files should eventually be renamed from `.py` to `.schema.json`.

## Where Commercial Platforms Still Lead

Mature commercial EMS, SCADA, and VPP platforms may already provide:

- Certified or field-tested ISO integrations.
- Existing PCS, inverter, meter, and SCADA drivers.
- 24/7 operational support.
- Cybersecurity programs and enterprise procurement packages.
- Live control workflows already validated at customer sites.
- Settlement, nominations, and market operations support.

ApexBEMS should not be positioned as replacing these capabilities today. Its near-term value is as an open, testable, safety-gated optimization and shadow-mode validation layer that can complement or precede production integration.

## Strategic Difference

Many commercial EMS platforms expose limited internal optimization detail to external reviewers. ApexBEMS is valuable because its control logic, audit trail, and contracts can be inspected, tested, and extended.

The strongest near-term positioning is:

> ApexBEMS is an open, testable, safety-gated shadow-mode foundation for market-aware energy dispatch across batteries and flexible compute loads.

## Practical Pilot Path

The most realistic pilot path is:

1. Ingest 30-90 days of historical site telemetry and market prices.
2. Replay ApexBEMS recommendations in shadow mode.
3. Compare actual site behavior against ApexBEMS recommendations.
4. Report estimated value difference, SOC safety, unsafe recommendation count, fallback count, and audit completeness.
5. Only after successful replay, move to signed dry-run commands.
6. Only after dry-run validation and operator approval, consider staged live hardware activation.

This keeps adoption low-risk because ApexBEMS can prove value before any live control path is enabled.

After live-read vendor telemetry drivers, 30-day private-site replay benchmarks, cryptographically signed dry-run command output, and staged live hardware activation are implemented, the stronger claim becomes:

> ApexBEMS is a pilot-ready operator decision engine for storage, compute load, and market participation.

In short: commercial EMS platforms may be stronger at field integration today; ApexBEMS is strongest where transparency, reproducibility, inspectable optimization, and safety-gated shadow-mode validation matter.
