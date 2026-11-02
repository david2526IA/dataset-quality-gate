# Dataset Quality Gate

A small schema-driven quality gate for CSV datasets. It validates required fields, basic types and numeric ranges, then writes accepted records, rejected records with reasons and a concise summary.

## Run

`schema.json`:

```json
{"asset_id":{"type":"string","required":true},"temperature":{"type":"number","min":-20,"max":120,"required":true}}
```

```bash
pip install .
dataset-quality-gate telemetry.csv schema.json
```

This creates `accepted.csv`, `rejected.jsonl` and `quality_summary.json` by default.

## Design

Rejected rows retain their original data and reasons so they can be investigated or corrected without silently disappearing. The tool performs validation only: it does not infer business rules, repair source data or replace data governance.

## Development

```bash
pip install ".[dev]"
pytest -q
```

## License

MIT
