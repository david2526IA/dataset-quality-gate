from dataset_quality_gate.gate import validate_rows


SCHEMA = {"asset_id": {"type": "string", "required": True}, "temperature": {"type": "number", "min": -20, "max": 120, "required": True}, "count": {"type": "integer"}}


def test_valid_and_invalid_rows_are_separated_with_reasons() -> None:
    report = validate_rows([{"asset_id": "PUMP-01", "temperature": "25.5", "count": "2"}, {"asset_id": "", "temperature": "150", "count": "2.5"}], SCHEMA)
    assert report["summary"] == {"accepted_rows": 1, "rejected_rows": 1, "total_rows": 2}
    reasons = {item["reason"] for item in report["rejected"][0]["reasons"]}
    assert {"required", "above maximum 120", "expected integer"} <= reasons


def test_missing_columns_are_reported() -> None:
    report = validate_rows([{"asset_id": "PUMP-01"}], SCHEMA)
    assert report["rejected"][0]["reasons"][0]["field"] == "temperature"
