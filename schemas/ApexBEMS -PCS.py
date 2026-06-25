{
"$schema": "https://json-schema.org/draft/2020-12/schema",
"$id": "https://apexbems.local/schemas/apexbems-pcs-command-v1.schema.json",
"title": "ApexBEMS_PCSCommand_v1",
"type": "object",
"additionalProperties": false,
"required": [
"schema_version",
"timestamp",
"site_id",
"dispatch_id",
"command_id",
"dry_run",
"setpoint_kw",
"ramp_seconds",
"reason",
"safety_status"
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
"expires_at": {
"type": "string",
"format": "date-time",
"description": "Command must not be executed after this time."
},
"ttl_seconds": {
"type": "integer",
"minimum": 1,
"description": "Maximum command lifetime from timestamp."
},
"site_id": {
"type": "string",
"minLength": 1
},
"pcs_id": {
"type": "string",
"description": "Optional PCS, inverter, battery string, or container identifier."
},
"dispatch_id": {
"type": "string",
"minLength": 1,
"description": "ID of the ApexBEMS dispatch decision that produced this command."
},
"command_id": {
"type": "string",
"minLength": 1,
"description": "Idempotency key for this command."
},
"dry_run": {
"type": "boolean",
"const": true,
"description": "Current implementation should emit dry-run commands only."
},
"command_type": {
"type": "string",
"enum": ["set_power", "charge", "discharge", "hold", "stop"],
"default": "set_power"
},
"setpoint_kw": {
"type": "number",
"description": "PCS power setpoint. Positive means discharge/export. Negative means charge/import."
},
"current_power_kw": {
"type": "number",
"description": "Current PCS power using the same sign convention as setpoint_kw."
},
"max_charge_kw": {
"type": "number",
"minimum": 0
},
"max_discharge_kw": {
"type": "number",
"minimum": 0
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
"ramp_seconds": {
"type": "integer",
"minimum": 0
},
"reason": {
"type": "string",
"minLength": 1
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
"operator_approval_required": {
"type": "boolean",
"default": true
},
"operator_override_active": {
"type": "boolean",
"default": false
},
"source_snapshot_hash": {
"type": "string",
"description": "Stable hash of the validated SiteTelemetryEnvelope/SiteSnapshot input."
},
"decision_hash": {
"type": "string",
"description": "Stable hash of the dispatch decision that generated this command."
},
"signature": {
"type": "object",
"additionalProperties": false,
"required": ["algorithm", "key_id", "value"],
"properties": {
"algorithm": {
"type": "string",
"enum": ["ed25519", "ecdsa-secp256k1", "hmac-sha256"]
},
"key_id": {
"type": "string"
},
"value": {
"type": "string"
}
}
}
},
"anyOf": [
{ "required": ["expires_at"] },
{ "required": ["ttl_seconds"] }
]
}
