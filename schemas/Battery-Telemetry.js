{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "PCSTelemetry_v1",
  "type": "object",
  "required": ["timestamp", "site_id", "soc", "power_kw", "temperature_c"],
  "properties": {
    "timestamp": { "type": "string", "format": "date-time" },
    "site_id": { "type": "string" },
    "soc": { "type": "number", "minimum": 0, "maximum": 1 },
    "power_kw": { "type": "number" },
    "temperature_c": { "type": "number" },
    "voltage_v": { "type": "number" },
    "current_a": { "type": "number" },
    "max_charge_kw": { "type": "number" },
    "max_discharge_kw": { "type": "number" },
    "bms_status": { "type": "string" }
  }
}
