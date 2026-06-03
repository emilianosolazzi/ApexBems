{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "BTCMarketFeed_v1",
  "type": "object",
  "required": ["timestamp", "btc_price_usd", "fee_rate_sat_per_vb"],
  "properties": {
    "timestamp": { "type": "string", "format": "date-time" },
    "btc_price_usd": { "type": "number", "minimum": 0 },
    "fee_rate_sat_per_vb": { "type": "number", "minimum": 0 }
  }
}
