{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "ApexBEMS_DispatchDecision_v1",
  "type": "object",
  "required": ["timestamp", "site_id", "dispatch_id", "p_mine_kw", "p_batt_kw"],
  "properties": {
    "timestamp": { "type": "string", "format": "date-time" },
    "site_id": { "type": "string" },
    "dispatch_id": { "type": "string" },
    "p_mine_kw": { "type": "number", "minimum": 0 },
    "p_batt_kw": { "type": "number" },
    "shadow_prices": {
      "type": "object",
      "additionalProperties": { "type": "number" }
    },
    "reason": { "type": "string" }
  }
}
