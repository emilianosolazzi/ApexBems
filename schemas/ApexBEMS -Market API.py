{
"$schema": "https://json-schema.org/draft/2020-12/schema",
"$id": "https://apexbems.local/schemas/apexbems-iso-bid-v1.schema.json",
"title": "ApexBEMS_ISOBid_v1",
"type": "object",
"additionalProperties": false,
"required": [
"schema_version",
"timestamp",
"site_id",
"dispatch_id",
"bid_id",
"dry_run",
"market",
"product",
"interval_start",
"bid_curve",
"price_unit",
"quantity_unit",
"policy_status"
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
"description": "Bid artifact must not be submitted after this time."
},
"ttl_seconds": {
"type": "integer",
"minimum": 1
},
"site_id": {
"type": "string",
"minLength": 1
},
"dispatch_id": {
"type": "string",
"minLength": 1,
"description": "ID of the ApexBEMS dispatch decision that produced this bid."
},
"bid_id": {
"type": "string",
"minLength": 1,
"description": "Idempotency key for this bid artifact."
},
"dry_run": {
"type": "boolean",
"const": true,
"description": "Current implementation should emit dry-run market bid artifacts only."
},
"market": {
"type": "string",
"enum": ["ERCOT", "CAISO", "PJM", "MISO", "NYISO", "ISO-NE", "SPP", "OTHER"]
},
"product": {
"type": "string",
"enum": ["energy", "reg_up", "reg_down", "spin", "non_spin", "capacity", "other"]
},
"interval_start": {
"type": "string",
"format": "date-time"
},
"interval_end": {
"type": "string",
"format": "date-time"
},
"price_unit": {
"type": "string",
"enum": ["USD_PER_MWH"],
"description": "External market bid price unit. Optimizer may use USD_PER_KWH internally, but bid artifacts should report ISO-facing USD/MWh unless an adapter says otherwise."
},
"quantity_unit": {
"type": "string",
"enum": ["KW", "MW"]
},
"bid_curve": {
"type": "array",
"minItems": 1,
"items": {
"type": "object",
"additionalProperties": false,
"required": ["price_usd_per_mwh", "quantity_kw"],
"properties": {
"price_usd_per_mwh": {
"type": "number"
},
"quantity_kw": {
"type": "number",
"description": "Positive quantity means export/discharge offer; negative quantity means import/charge bid if the target market/product supports it."
}
}
}
},
"policy_status": {
"type": "string",
"enum": ["allowed", "blocked", "requires_operator_review"]
},
"policy_reasons": {
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
"description": "Stable hash of the SiteTelemetryEnvelope/SiteSnapshot used as input."
},
"decision_hash": {
"type": "string",
"description": "Stable hash of the ApexBEMS dispatch decision that generated this bid."
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
