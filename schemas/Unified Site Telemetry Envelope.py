{
"$schema": "https://json-schema.org/draft/2020-12/schema",
"$id": "https://apexbems.local/schemas/site-telemetry-envelope-v1.schema.json",
"title": "SiteTelemetryEnvelope_v1",
"type": "object",
"additionalProperties": false,
"required": [
"schema_version",
"timestamp",
"site_id",
"ingestion_id",
"streams"
],
"properties": {
"schema_version": {
"type": "string",
"const": "1.0"
},
"timestamp": {
"type": "string",
"format": "date-time",
"description": "Envelope creation time. Individual streams may have their own timestamps."
},
"site_id": {
"type": "string",
"minLength": 1
},
"ingestion_id": {
"type": "string",
"minLength": 1,
"description": "Unique ID for this normalized telemetry snapshot."
},
"source": {
"type": "string",
"description": "Replay, live adapter, CSV import, SCADA export, or test fixture."
},
"streams": {
"type": "object",
"additionalProperties": false,
"required": [
"miner",
"pcs",
"market",
"btc"
],
"properties": {
"miner": {
"$ref": "./miner-telemetry-v1.schema.json"
},
"pcs": {
"$ref": "./pcs-telemetry-v1.schema.json"
},
"market": {
"$ref": "./market-price-feed-v1.schema.json"
},
"btc": {
"$ref": "./btc-market-feed-v1.schema.json"
},
"meter": {
"$ref": "./meter-telemetry-v1.schema.json"
},
"breaker": {
"$ref": "./breaker-state-v1.schema.json"
},
"transformer": {
"$ref": "./transformer-state-v1.schema.json"
},
"feeder": {
"$ref": "./feeder-constraint-v1.schema.json"
},
"alarms": {
"type": "array",
"items": {
"$ref": "./site-alarm-v1.schema.json"
}
},
"curtailment": {
"$ref": "./curtailment-state-v1.schema.json"
},
"operator_override": {
"$ref": "./operator-override-v1.schema.json"
}
}
},
"site_limits": {
"type": "object",
"additionalProperties": false,
"properties": {
"transformer_limit_kw": {
"type": "number",
"minimum": 0
},
"grid_import_limit_kw": {
"type": "number",
"minimum": 0
},
"grid_export_limit_kw": {
"type": "number",
"minimum": 0
},
"interconnection_limit_kw": {
"type": "number",
"minimum": 0
}
}
},
"quality": {
"type": "object",
"additionalProperties": false,
"properties": {
"is_replay": {
"type": "boolean",
"default": false
},
"missing_streams": {
"type": "array",
"items": {
"type": "string"
}
},
"stale_streams": {
"type": "array",
"items": {
"type": "string"
}
},
"validation_warnings": {
"type": "array",
"items": {
"type": "string"
}
}
}
}
}
}
