{
"$schema": "https://json-schema.org/draft/2020-12/schema",
"$id": "https://apexbems.local/schemas/btc-market-feed-v1.schema.json",
"title": "BTCMarketFeed_v1",
"type": "object",
"additionalProperties": false,
"required": [
"schema_version",
"timestamp",
"source",
"btc_price_usd",
"network_hashrate_ehs",
"difficulty",
"estimated_fee_rate_sat_per_vb"
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
"source": {
"type": "string",
"description": "Data source such as Coinbase, mempool.space, Luxor, Hashrate Index, custom oracle, CSV replay, or fixture."
},
"btc_price_usd": {
"type": "number",
"exclusiveMinimum": 0
},
"network_hashrate_ehs": {
"type": "number",
"exclusiveMinimum": 0,
"description": "Estimated Bitcoin network hashrate in EH/s."
},
"difficulty": {
"type": "number",
"exclusiveMinimum": 0
},
"block_height": {
"type": "integer",
"minimum": 0
},
"block_subsidy_btc": {
"type": "number",
"minimum": 0,
"description": "Current block subsidy in BTC."
},
"avg_recent_fees_btc_per_block": {
"type": "number",
"minimum": 0,
"description": "Average recent transaction fees per block in BTC."
},
"expected_reward_btc_per_block": {
"type": "number",
"minimum": 0,
"description": "Block subsidy plus expected transaction fees."
},
"estimated_fee_rate_sat_per_vb": {
"type": "number",
"minimum": 0
},
"hashprice_usd_per_ph_day": {
"type": "number",
"minimum": 0,
"description": "Optional externally reported hashprice. If absent, ApexBEMS can compute a proxy from price, hashrate, subsidy, and fees."
},
"observed_window_blocks": {
"type": "integer",
"minimum": 1,
"description": "Number of recent blocks used to estimate fees or hashrate."
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
