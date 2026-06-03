{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "MarketPriceFeed_v1",
  "type": "object",
  "required": ["timestamp", "market", "interval_start", "price"],
  "properties": {
    "timestamp": { "type": "string", "format": "date-time" },
    "market": { "type": "string" },
    "interval_start": { "type": "string", "format": "date-time" },
    "price": { "type": "number" },
    "confidence": { "type": "number", "minimum": 0, "maximum": 1 }
  }
}
