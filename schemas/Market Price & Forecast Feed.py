{
"$schema": "https://json-schema.org/draft/2020-12/schema",
"$id": "https://apexbems.local/schemas/market-price-feed-v1.schema.json",
"title": "MarketPriceFeed_v1",
"type": "object",
"additionalProperties": false,
"required": [
"schema_version",
"timestamp",
"source",
"market",
"product",
"interval_start",
"price",
"price_unit"
],
"properties": {
"schema_version": {
"type": "string",
"const": "1.0"
},
"timestamp": {
"type": "string",
"format": "date-time",
"description": "Time this market feed record was produced or ingested."
},
"source": {
"type": "string",
"description": "Data source such as ERCOT, CAISO, PJM, CSV replay, fixture, vendor API, or forecast service."
},
"market": {
"type": "string",
"enum": ["ERCOT", "CAISO", "PJM", "MISO", "NYISO", "ISO-NE", "SPP", "OTHER"]
},
"node": {
"type": "string",
"description": "Settlement point, hub, node, zone, or pricing location."
},
"product": {
"type": "string",
"enum": ["energy", "reg_up", "reg_down", "spin", "non_spin", "capacity", "other"]
},
"market_type": {
"type": "string",
"enum": ["real_time", "day_ahead", "forecast", "settlement", "other"]
},
"interval_start": {
"type": "string",
"format": "date-time"
},
"interval_end": {
"type": "string",
"format": "date-time"
},
"interval_minutes": {
"type": "number",
"exclusiveMinimum": 0
},
"price": {
"type": "number",
"description": "Reported price using price_unit. Negative prices are allowed."
},
"price_unit": {
"type": "string",
"enum": ["USD_PER_MWH", "USD_PER_KWH"],
"description": "External reported price unit. ApexBEMS should normalize to USD_PER_KWH internally."
},
"optimizer_price_usd_per_kwh": {
"type": "number",
"description": "Optional normalized optimizer price. Required by semantic validation before optimizer input."
},
"mwh_to_kwh_conversion_applied": {
"type": "boolean",
"description": "True when price_unit was USD_PER_MWH and optimizer_price_usd_per_kwh was computed by dividing by 1000."
},
"confidence": {
"type": "number",
"minimum": 0,
"maximum": 1,
"description": "Optional confidence for forecasted prices."
},
"is_forecast": {
"type": "boolean",
"default": false
},
"quality": {
"type": "object",
"additionalProperties": false,
"properties": {
"is_replay": {
"type": "boolean",
"default": false
},
"stale": {
"type": "boolean",
"default": false
},
"warnings": {
"type": "array",
"items": {
"type": "string"
}
}
}
}
}
}
