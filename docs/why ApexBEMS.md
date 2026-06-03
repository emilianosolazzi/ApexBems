1. The “Brain” — Forecasting Ensemble

ApexBEMS doesn’t guess future prices. It builds a multi‑model forecast using:

    LSTM neural networks

    Prophet (seasonality model)

    XGBoost (tree‑based regression)

Each model produces a prediction.
ApexBEMS then uses Bayesian Regret weighting to give more influence to whichever model has been most accurate recently.

Why this matters:  
The system is always learning which forecaster is “hot” and shifts weight accordingly — a self‑optimizing ensemble.

Explore: forecasting ensemble
2. The “Rules” — MPC Optimization Engine

Once the forecast is ready, ApexBEMS uses Model Predictive Control (MPC) — the same technique used in aerospace and high‑frequency trading.

Think of it like driving:

    You don’t steer based only on what’s directly in front of you.

    You look ahead, anticipate curves, and adjust early.

ApexBEMS does the same:

    If prices will spike in 2 hours → charge now

    If prices will crash → discharge now

    If regulation markets look profitable → reserve headroom

The SOS2 “wear‑and‑tear” model

Charging/discharging a battery causes degradation.
ApexBEMS uses SOS2 piecewise‑linear degradation curves to model:

    cycle aging

    temperature effects

    depth‑of‑discharge penalties

This ensures the optimizer never destroys the battery chasing tiny profits.

Explore: MPC optimization
3. The “Accountant” — Explainability & Audit Trail

ApexBEMS is autonomous, but never a black box.

Every dispatch decision is logged in:
Code

audit_log.db

Each entry includes:

    the action taken

    the reason

    the shadow prices (constraint bottlenecks)

    the SHAP feature importance

    the bid curve used

    SOC, temperature, cycle count

This creates a forensic‑grade ledger of every decision.

Why this matters:  
Operators, regulators, and investors can always answer:

    “Why did the system charge here?”

    “Why did it curtail mining?”

    “Which constraint was binding?”
