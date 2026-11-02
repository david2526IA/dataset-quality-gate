from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from .gate import validate_rows


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate a CSV file against a compact JSON schema.")
    parser.add_argument("input", type=Path)
    parser.add_argument("schema", type=Path)
    parser.add_argument("--accepted", type=Path, default=Path("accepted.csv"))
    parser.add_argument("--rejected", type=Path, default=Path("rejected.jsonl"))
    parser.add_argument("--summary", type=Path, default=Path("quality_summary.json"))
    args = parser.parse_args()
    with args.input.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
        fieldnames = handle.seek(0) or next(csv.reader(handle))
    report = validate_rows(rows, json.loads(args.schema.read_text(encoding="utf-8")))
    with args.accepted.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(report["accepted"])
    args.rejected.write_text("".join(json.dumps(row) + "\n" for row in report["rejected"]), encoding="utf-8")
    args.summary.write_text(json.dumps(report["summary"], indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report["summary"]))
