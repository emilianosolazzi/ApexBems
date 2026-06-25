{
"$schema": "https://json-schema.org/draft/2020-12/schema",
"$id": "https://apexbems.local/schemas/apexbems-dispatch-decision-v1.schema.json",
"title": "ApexBEMS_DispatchDecision_v1",
"type": "object",
"additionalProperties": false,
"required": [
"schema_version",
"timestamp",
"site_id",
"dispatch_id",
"control_mode",
"source_snapshot_hash",
"optimizer_status",
"safe_fallback",
"p_batt_kw",
"p_mine_kw",
"safety_status",
"reason"
],
"properties": {
"schema_version": {
"type": "string",
"const": "1.0"
},
"timestamp": {
"type": "string",
"format": "date-time"
},
"site_id": {
"type": "string",
"minLength": 1
},
"dispatch_id": {
"type": "string",
"minLength": 1
},
"control_mode": {
"type": "string",
"enum": ["shadow", "dry_run", "live_blocked"],
"description": "Current repository should emit shadow or dry_run decisions only."
},
"source_snapshot_hash": {
"type": "string",
"minLength": 1,
"description": "Stable hash of the SiteTelemetryEnvelope or normalized SiteSnapshot used as optimizer input."
},
"decision_hash": {
"type": "string",
"description": "Stable canonical hash of this dispatch decision excluding signature fields."
},
"optimizer_status": {
"type": "string",
"enum": ["optimal", "feasible", "infeasible", "error", "fallback"]
},
"safe_fallback": {
"type": "boolean",
"description": "True when ApexBEMS intentionally chose a safe hold/fallback action."
},
"p_batt_kw": {
"type": "number",
"description": "Battery/PCS setpoint. Positive means discharge/export. Negative means charge/import."
},
"p_mine_kw": {
"type": "number",
"minimum": 0,
"description": "Recommended mining load in kW."
},
"current_soc": {
"type": "number",
"minimum": 0,
"maximum": 1
},
"projected_soc": {
"type": "number",
"minimum": 0,
"maximum": 1
},
"soc_min": {
"type": "number",
"minimum": 0,
"maximum": 1
},
"soc_max": {
"type": "number",
"minimum": 0,
"maximum": 1
},
"market_price_usd_per_kwh": {
"type": "number",
"description": "Optimizer-normalized market price."
},
"reported_market_price_usd_per_mwh": {
"type": "number",
"description": "Original market price when source reports in $/MWh."
},
"mwh_to_kwh_conversion_applied": {
"type": "boolean"
},
"btc_price_usd": {
"type": "number",
"minimum": 0
},
"mining_break_even_usd_per_mwh": {
"type": "number"
},
"expected_storage_value_usd": {
"type": "number"
},
"expected_mining_value_usd": {
"type": "number"
},
"expected_total_value_usd": {
"type": "number"
},
"objective_usd": {
"type": "number"
},
"safety_status": {
"type": "string",
"enum": ["allowed", "blocked", "requires_operator_review"]
},
"safety_reasons": {
"type": "array",
"items": {
"type": "string"
}
},
"soc_violation_before_clipping": {
"type": "boolean"
},
"soc_clipping_event": {
"type": "boolean"
},
"operator_override_active": {
"type": "boolean",
"default": false
},
"shadow_prices": {
"type": "object",
"additionalProperties": {
"type": "number"
}
},
"bid_curve": {
"type": "array",
"items": {
"type": "object",
"additionalProperties": false,
"required": ["price_usd_per_mwh", "quantity_kw"],
"properties": {
"price_usd_per_mwh": {
"type": "number"
},
"quantity_kw": {
"type": "number"
}
}
}
},
"generated_command_ids": {
"type": "array",
"description": "Command IDs for dry-run PCS/miner command artifacts generated from this decision.",
"items": {
"type": "string"
}
},
"reason": {
"type": "string",
"minLength": 1
},
"metadata": {
"type": "object",
"additionalProperties": false,
"properties": {
"horizon_steps": {
"type": "integer",
"minimum": 1
},
"scenario_count": {
"type": "integer",
"minimum": 1
},
"solver": {
"type": "string"
},
"seed": {
"type": "integer"
}
}
}
}
}
