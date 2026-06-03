{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "ApexBEMS_ISOBid_v1",
  "type": "object",
  "required": ["timestamp", "site_id", "market", "product", "interval_start", "bid_curve"],
  "properties": {
    "timestamp": { "type": "string", "format": "date-time" },
    "site_id": { "type": "string" },
    "market": { "type": "string" },
    "product": { "type": "string" },
    "interval_start": { "type": "string", "format": "date-time" },
    "bid_curve": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["price", "quantity_kw"],
        "properties": {
          "price": { "type": "number" },
          "quantity_kw": { "type": "number" }
        }
      }
    }
  }
}
