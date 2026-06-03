{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "SiteTelemetryEnvelope_v1",
  "type": "object",
  "required": ["timestamp", "site_id", "streams"],
  "properties": {
    "timestamp": { "type": "string", "format": "date-time" },
    "site_id": { "type": "string" },
    "streams": {
      "type": "object",
      "properties": {
        "miner": { "$ref": "MinerTelemetry_v1" },
        "pcs": { "$ref": "PCSTelemetry_v1" },
        "market": { "$ref": "MarketPriceFeed_v1" },
        "btc": { "$ref": "BTCMarketFeed_v1" }
      }
    }
  }
}
