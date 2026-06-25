{
"$schema": "https://json-schema.org/draft/2020-12/schema",
"$id": "https://apexbems.local/schemas/miner-telemetry-v1.schema.json",
"title": "MinerTelemetry_v1",
"type": "object",
"additionalProperties": false,
"required": [
"schema_version",
"timestamp",
"site_id",
"source",
"power_kw",
"hashrate_ths",
"avg_temp_c",
"status"
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
"fleet_id": {
"type": "string",
"description": "Optional miner fleet, container, room, or group identifier."
},
"source": {
"type": "string",
"description": "Telemetry source such as Foreman, LuxOS, Braiins, custom RPC, CSV replay, or manual import."
},
"status": {
"type": "string",
"enum": ["online", "degraded", "curtailed", "offline", "unknown"]
},
"power_kw": {
"type": "number",
"minimum": 0
},
"available_power_kw": {
"type": "number",
"minimum": 0,
"description": "Power that can be allocated to mining under current site conditions."
},
"max_power_kw": {
"type": "number",
"minimum": 0,
"description": "Configured miner fleet power limit."
},
"hashrate_ths": {
"type": "number",
"minimum": 0
},
"efficiency_j_per_th": {
"type": "number",
"exclusiveMinimum": 0
},
"avg_temp_c": {
"type": "number"
},
"max_temp_c": {
"type": "number"
},
"fan_speed_pct": {
"type": "number",
"minimum": 0,
"maximum": 100
},
"active_miners": {
"type": "integer",
"minimum": 0
},
"total_miners": {
"type": "integer",
"minimum": 0
},
"uptime_pct": {
"type": "number",
"minimum": 0,
"maximum": 100
},
"rejected_hashrate_pct": {
"type": "number",
"minimum": 0,
"maximum": 100
},
"pool_difficulty": {
"type": "number",
"minimum": 0
},
"curtailment_allowed": {
"type": "boolean",
"default": true
},
"operator_override": {
"type": "boolean",
"default": false
},
"observed_interval_sec": {
"type": "integer",
"minimum": 1,
"description": "Telemetry aggregation window in seconds."
}
}
}
