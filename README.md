# ApexBEMS v7.0

**Fully Autonomous, Explainable, Market-Ready Battery Energy Management System**

[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

A production-grade Battery Energy Management System (BEMS) that autonomously optimizes grid-scale battery storage across multiple electricity markets. Features explainable AI, real-time market bidding, and self-optimizing ensemble forecasting.

---

## 🚀 Key Features

### Core Capabilities
- **SOS2 Piecewise Degradation Modeling** — Exact piecewise linear cost functions for battery degradation
- **Cyclic Feature Encoding** — sin/cos temporal encoding for hour, day-of-week, and month patterns
- **Persistent State Management** — JSON-based state persistence across restarts
- **Event-Driven Architecture** — Decoupled components via EventBus pub/sub pattern
- **Self-Optimizing Ensemble** — Bayesian softmax regret for dynamic forecast weight tuning
- **Parametric Bid Curves** — Automated price-quantity pair generation for market submission
- **Policy Validation** — Pre-submission sanity checks for bid feasibility
- **Explainable Dispatch** — SHAP feature importance and shadow price bottleneck analysis

### Forecasting
- Multi-model ensemble: LSTM (with attention), Prophet, XGBoost
- VAE scenario generation for uncertainty quantification
- Automatic drift detection with retraining triggers
- Dynamic horizon adjustment based on market volatility

### Market Integration
- Multi-market optimization (Energy, Regulation Up/Down, Spinning Reserve)
- Multi-bandit exploration for strategy refinement
- Tiered imbalance penalty modeling
- Simulated market API with retry logic

### Monitoring & Auditing
- SQLite audit logging with shadow prices and feature importance
- Bottleneck analysis via constraint shadow prices
- Real-time drift detection and ensemble weight adaptation
- Structured dispatch logging for regulatory compliance

---

## 📋 Prerequisites

### Required
- Python 3.8+
- NumPy, Pandas, PuLP, scikit-learn

### Optional (Enhanced Features)
- **TensorFlow** — LSTM forecasting with attention mechanism
- **Prophet** — Time series decomposition and trend forecasting
- **XGBoost** — Gradient-boosted tree forecasting
- **SHAP** — Feature importance explanations

---

## ⚙️ Installation

```bash
# Clone repository
git clone https://github.com/yourusername/apex-bems.git
cd apex-bems

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Install core dependencies
pip install numpy pandas pulp scikit-learn python-dateutil

# Install optional dependencies (recommended)
pip install tensorflow prophet xgboost shap

 Quick Start
import asyncio
from apex_bems import BEMSConfig, MPController, main_services

async def run():
    # Initialize configuration
    cfg = BEMSConfig(
        capacity_kwh=1000.0,
        max_power_kw=250.0,
        market='ERCOT',
        products=['energy', 'reg_up', 'reg_down', 'spin']
    )
    
    # Initialize services and controller
    mpc = main_services(cfg)
    
    # Run simulation steps
    for step in range(100):
        plan = await mpc.step()
        print(f"Dispatch: {plan.action_kw:.1f} kW — {plan.reason}")

asyncio.run(run())

Architecture
┌─────────────────────────────────────────────────────┐
│                    Event Bus                         │
├──────────┬──────────┬──────────┬──────────┬─────────┤
│Forecaster│Optimizer │Battery   │Monitor   │Market   │
│ Service  │ Service  │ State    │ Service  │API      │
│          │          │ Service  │          │Client   │
├──────────┴──────────┴──────────┴──────────┴─────────┤
│                   MPC Controller                     │
├─────────────────────────────────────────────────────┤
│    Policy Validator    │    Audit Logger (SQLite)    │
└─────────────────────────────────────────────────────┘

Component Overview

Component	Responsibility
ForecasterService	Multi-model ensemble prediction, VAE scenario generation
OptimizationService	Multi-market stochastic optimization, parametric bid curves
BatteryStateService	State tracking, SOS2 degradation costs, temperature effects
MonitoringService	Drift detection, horizon adjustment, exploration triggering
MarketAPIClient	Market data retrieval, bid submission with retry logic
PolicyValidator	Pre-submission bid feasibility checks
AuditLogger	Structured dispatch logging with explainability metadata
EventBus	Decoupled inter-component communication

Configuration

Key configuration parameters in BEMSConfig:
Parameter	Default	Description
capacity_kwh	1000.0	Battery energy capacity
max_power_kw	250.0	Maximum charge/discharge power
horizon_hours	4	Optimization horizon
max_scenarios	100	Monte Carlo scenarios
solver	'CBC'	Optimization solver (CBC/Gurobi/CPLEX/HiGHS)
bid_price_tiers	10	Parametric sweep granularity
confidence	0.95	Risk-adjusted optimization
drift_mae_sigma	1.5	Drift detection sensitivity

Output & Logging
Dispatch Log (SQLite)

Each dispatch decision is logged with:

    Timestamp, action (kW), state of charge

    Active shadow prices and constraints

    Top SHAP feature importances

    Submitted bid curve

    Battery health metrics (temperature, cycle count)

Bottleneck Analysis
# Get top constraints limiting revenue
bottlenecks = audit.get_bottlenecks(limit=5)
print(bottlenecks)
# [('soc_max_t3', 45.2), ('ramp_up_t7', 32.1), ...]

Real-time Monitoring

    Drift alerts when prediction MAE exceeds threshold

    Automatic model retraining triggers

    Horizon adjustment based on volatility regime

Testing
# Run with simulated market data
python apex_bems.py

# Enable debug logging
python apex_bems.py --log-level DEBUG

# Specify solver
python apex_bems.py --solver GUROBI --time-limit 60

Performance Optimizations

    Solver Selection: Use commercial solvers (Gurobi/CPLEX) for large-scale problems

    Scenario Reduction: Adjust max_scenarios based on computational budget

    Incremental Training: Models retrain only on schedule or drift detection

    Persistent State: Minimizes cold-start delays after restarts

 Advanced Features
Custom Ensemble Weights

# For commercial solver support (optional)
# Gurobi: Follow Gurobi installation guide
# CPLEX: Follow IBM CPLEX installation guide

forecaster.ensemble.weights = {'lstm': 0.5, 'prophet': 0.2, 'xgb': 0.3}
forecaster.ensemble.temperature = 0.1  # Sharper weight distribution

Multi-Bandit Exploration
python

cfg.exploration_prob = 0.15  # 15% chance to explore alternative strategies

Temperature-Dependent Degradation
python

cfg.activation_energy_ev = 0.5  # Arrhenius model parameter
cfg.temperature_ref = 25.0      # Reference temperature (°C)

 Reference

The system implements state-of-the-art techniques from:

    Stochastic Dual Dynamic Programming for multi-stage optimization

    Bayesian Model Averaging for ensemble forecasting

    Shapley Additive Explanations for dispatch explainability

    Arrhenius Degradation Models for battery health tracking

 License

MIT License — See LICENSE for details.
 Contributing

Contributions welcome! Areas of interest:

    Additional market product support

    Alternative forecasting architectures

    Hardware-in-the-loop integration

    Real market API connectors

 Contact

For questions or commercial licensing, contact emiliano.arlington@gmail.com, coma.retained@gmail.com

Built for production energy trading operations with explainability and regulatory compliance as first-class requirements.



