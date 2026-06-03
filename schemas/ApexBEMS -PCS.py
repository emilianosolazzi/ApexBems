{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "ApexBEMS_PCSCommand_v1",
  "type": "object",
  "required": ["timestamp", "site_id", "command_id", "setpoint_kw"],
  "properties": {
    "timestamp": { "type": "string", "format": "date-time" },
    "site_id": { "type": "string" },
    "command_id": { "type": "string" },
    "setpoint_kw": { "type": "number" },
    "ramp_seconds": { "type": "number", "minimum": 0 },
    "reason": { "type": "string" }
  }
}
