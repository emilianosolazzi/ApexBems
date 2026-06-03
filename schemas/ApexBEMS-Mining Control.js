{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "ApexBEMS_MinerCommand_v1",
  "type": "object",
  "required": ["timestamp", "site_id", "command_id", "target_power_kw"],
  "properties": {
    "timestamp": { "type": "string", "format": "date-time" },
    "site_id": { "type": "string" },
    "command_id": { "type": "string" },
    "target_power_kw": { "type": "number", "minimum": 0 },
    "ramp_seconds": { "type": "number", "minimum": 0 },
    "reason": { "type": "string" }
  }
}
