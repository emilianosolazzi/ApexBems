{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "MinerTelemetry_v1",
  "type": "object",
  "required": ["timestamp", "site_id", "power_kw", "hashrate_ths", "avg_temp_c"],
  "properties": {
    "timestamp": { "type": "string", "format": "date-time" },
    "site_id": { "type": "string" },
    "power_kw": { "type": "number", "minimum": 0 },
    "hashrate_ths": { "type": "number", "minimum": 0 },
    "avg_temp_c": { "type": "number" },
    "efficiency_j_per_th": { "type": "number", "minimum": 0 },
    "fan_speed_pct": { "type": "number", "minimum": 0, "maximum": 100 },
    "active_miners": { "type": "integer", "minimum": 0 },
    "pool_difficulty": { "type": "number", "minimum": 0 }
  }
}
