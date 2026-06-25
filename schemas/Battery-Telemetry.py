{
"$schema": "https://json-schema.org/draft/2020-12/schema",
"$id": "https://apexbems.local/schemas/pcs-telemetry-v1.schema.json",
"title": "PCSTelemetry_v1",
"type": "object",
"additionalProperties": false,
"required": [
"schema_version",
"timestamp",
"site_id",
"soc",
"power_kw",
"temperature_c",
"status"
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
"site_id": {
"type": "string",
"minLength": 1
},
"pcs_id": {
"type": "string",
"description": "Optional PCS, inverter, battery string, or container identifier."
},
"source": {
"type": "string",
"description": "Telemetry source such as Modbus, SunSpec, SCADA, vendor API, CSV replay, or manual import."
},
"status": {
"type": "string",
"enum": ["online", "standby", "charging", "discharging", "faulted", "offline", "unknown"]
},
"available": {
"type": "boolean",
"default": true,
"description": "Whether the PCS is currently available for optimization recommendations."
},
"soc": {
"type": "number",
"minimum": 0,
"maximum": 1
},
"soc_min": {
"type": "number",
"minimum": 0,
"maximum": 1,
"description": "Current lower SOC safety limit for this PCS/battery."
},
"soc_max": {
"type": "number",
"minimum": 0,
"maximum": 1,
"description": "Current upper SOC safety limit for this PCS/battery."
},
"soh": {
"type": "number",
"minimum": 0,
"maximum": 1,
"description": "State of health as a fraction of nameplate capacity."
},
"power_kw": {
"type": "number",
"description": "Current PCS power. Use positive for discharge/export and negative for charge/import."
},
"max_charge_kw": {
"type": "number",
"minimum": 0
},
"max_discharge_kw": {
"type": "number",
"minimum": 0
},
"ramp_rate_kw_per_min": {
"type": "number",
"minimum": 0,
"description": "Maximum PCS setpoint change rate in kW per minute."
},
"ramp_seconds": {
"type": "number",
"minimum": 0,
"description": "Approximate full-scale PCS ramp duration in seconds."
},
"charge_enabled": {
"type": "boolean",
"default": true
},
"discharge_enabled": {
"type": "boolean",
"default": true
},
"charge_discharge_mode": {
"type": "string",
"enum": ["unrestricted", "charge_only", "discharge_only", "idle_only", "standby", "unknown"],
"description": "Current PCS operating permission mode for recommendation safety checks."
},
"energy_capacity_kwh": {
"type": "number",
"exclusiveMinimum": 0
},
"temperature_c": {
"type": "number"
},
"max_cell_temperature_c": {
"type": "number"
},
"voltage_v": {
"type": "number",
"minimum": 0
},
"current_a": {
"type": "number"
},
"frequency_hz": {
"type": "number",
"minimum": 0
},
"bms_status": {
"type": "string"
},
"alarm_active": {
"type": "boolean",
"default": false
},
"fault_code": {
"type": "string"
},
"operator_override": {
"type": "boolean",
"default": false
},
"observed_interval_sec": {
"type": "integer",
"minimum": 1,
"description": "Telemetry aggregation interval in seconds."
}
}
}
