<div align="center">

# ApexBEMS v7.0

**Fully Autonomous · Explainable · Market-Ready Energy Management System**

[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![Status](https://img.shields.io/badge/status-production--ready-brightgreen.svg)]()
[![Contact](https://img.shields.io/badge/contact-request%20access-orange.svg)](mailto:emiliano.arlington@gmail.com)

ApexBEMS is the only platform that unifies **stochastic MPC**, **native multi-asset optimization**, **explainable AI**, and **autonomous market bidding** into a single, coherent production system.

*Enterprise licensing and site-specific deployments available — [Request Access](#contact)*

</div>

---

## Table of Contents

- [Key Features](#key-features)
- [System Architecture](#system-architecture)
- [Target Use Cases](#target-use-cases)
- [Configuration & Monitoring](#configuration--monitoring)
- [Scientific Foundations](#scientific-foundations)
- [License](#license)
- [Contact](#contact)

---

## Key Features

### Core Capabilities

| Feature | Description |
|---|---|
| **Stochastic MPC** | Monte Carlo optimization with volatility-aware horizon adjustment |
| **Multi-Asset Orchestration** | Unified control for batteries, flexible compute loads (ASICs/GPUs), and generators |
| **SOS2 Degradation Modeling** | Exact piecewise-linear cost curves for battery health and lifecycle protection |
| **Explainable Dispatch** | Per-dispatch SHAP feature importance and shadow-price audit logs |
| **Autonomous Bidding** | Parametric bid curves generated directly from the MPC engine |
| **Event-Driven Architecture** | Sub-second load modulation via asynchronous EventBus |
| **Policy Validation** | Pre-submission feasibility checks to ensure safe hardware operation |

### Forecasting & Intelligence

| Feature | Description |
|---|---|
| **Ensemble Forecaster** | Bayesian softmax regret weighting across LSTM (attention), Prophet, and XGBoost |
| **Drift Detection** | Automatic retraining triggered by forecast error thresholds |
| **Uncertainty Quantification** | VAE-based scenario generation for risk-adjusted dispatch |

### Auditing & Compliance

| Feature | Description |
|---|---|
| **Structured Ledger** | SQLite-backed audit logs capturing state, shadow prices, and decision rationale |
| **Bottleneck Analysis** | Real-time identification of limiting constraints (SOC, thermal, ramping) |
| **Regulatory Readiness** | Full transparency for enterprise risk and compliance teams |

---

## System Architecture

```
┌─────────────────────────────────────────────────────┐
│                    Event Bus                         │
├──────────┬──────────┬──────────┬──────────┬─────────┤
│Forecaster│Optimizer │Battery   │Monitor   │Market   │
│ Service  │ Service  │ State    │ Service  │ Client  │
├──────────┴──────────┴──────────┴──────────┴─────────┤
│                   MPC Controller                     │
├─────────────────────────────────────────────────────┤
│   Policy Validator       │   Audit Logger (SQLite)   │
└─────────────────────────────────────────────────────┘
```

| Component | Responsibility |
|---|---|
| `ForecasterService` | Multi-model ensemble prediction, VAE scenario generation |
| `OptimizationService` | Multi-market stochastic LP, parametric bid curves, scenario reduction |
| `BatteryStateService` | SOC tracking, SOS2 degradation costs, thermal derating |
| `MonitoringService` | Drift detection, dynamic horizon, bandit exploration |
| `MarketAPIClient` | Price data retrieval, bid submission with retry logic |
| `PolicyValidator` | Pre-submission bid feasibility checks |
| `AuditLogger` | Structured dispatch logging with explainability metadata |
| `EventBus` | Async-aware pub/sub for decoupled inter-component communication |

---

## Target Use Cases

| Sector | Value Proposition |
|---|---|
| **Grid-Scale Storage Operators** | Maximize revenue through intelligent arbitrage, regulation, and multi-market stacking |
| **Compute Facilities (Bitcoin/AI)** | Transform data centers into grid-stabilizing assets with sub-second compute modulation |
| **Regulated Entities** | Maintain audit-ready decision trails for all algorithmic market participation |

---

## Configuration & Monitoring

All behavior is controlled through `BEMSConfig`:

| Parameter | Default | Description |
|---|---|---|
| `capacity_kwh` | `1000.0` | Asset storage capacity |
| `max_power_kw` | `250.0` | Max charge/discharge power |
| `horizon_hours` | `4` | MPC look-ahead window |
| `max_scenarios` | `100` | Monte Carlo scenario count |
| `scenario_reduction_k` | `20` | k-medoids reduction for LP tractability |
| `solver` | `"CBC"` | Optimization backend (CBC, Gurobi, CPLEX, HiGHS) |
| `confidence` | `0.95` | Risk-adjusted optimization parameter |
| `temp_max_c` | `45.0` | Max cell temperature before hard cutoff (°C) |
| `temp_derate_start_c` | `35.0` | Temperature at which power derating begins (°C) |

### Bottleneck Analysis

```python
# Extract top constraints currently limiting revenue
bottlenecks = audit.get_bottlenecks(limit=5)
# [('soc_max_t3', 45.2), ('ramp_up_t7', 32.1), ...]
```

### Quick Start

```python
import asyncio
from apex_bems import BEMSConfig, main_services

async def run():
    cfg = BEMSConfig(
        capacity_kwh=1000.0,
        max_power_kw=250.0,
        market="ERCOT",
        solver="CBC",
    )
    mpc = main_services(cfg)   # validates config, wires all services

    for step in range(100):
        plan = await mpc.step(current_time, market_data)
        print(f"Dispatch: {plan.action_kw:+.1f} kW | SOC: {plan.soc:.1%} | {plan.reason}")

asyncio.run(run())
```

---

## Scientific Foundations

ApexBEMS implements state-of-the-art methods from:

- **Stochastic Dual Dynamic Programming** — multi-stage market optimization
- **Bayesian Model Averaging** — high-precision ensemble forecasting
- **SHAP Explainability** — post-hoc dispatch interpretation
- **Arrhenius Degradation Models** — physics-grounded battery aging
- **k-Medoids Scenario Reduction** — LP tractability without sacrificing stochastic coverage
- **McCormick Relaxation** — linearised thermal derating constraints

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

## Contact

To request access, provide site details and technical objectives:

| Role | Email |
|---|---|
| Primary | [emiliano.arlington@gmail.com](mailto:emiliano.arlington@gmail.com) |
| Secondary | [coma.retained@gmail.com](mailto:coma.retained@gmail.com) |

---

<div align="center">

*Built for production energy trading — explainability and regulatory compliance as first-class requirements.*

</div>
