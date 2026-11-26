"""Validate M14.9 record contracts and compare explicitly supplied observations."""
import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[3]


def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def validate_records():
    schema = read(ROOT / "docs/architecture/windows-app-records-v1.schema.json")
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)
    app_id = "a" * 32
    digest = "b" * 64
    owner = {"app_id": app_id, "user_id": "c" * 32, "generation": 1}
    source = {"sha256": digest, "publisher": "Test", "version": "1"}
    manifest = {"schema_version": 1, "owner": owner, "architecture": "x64",
                "source": source, "components": []}
    transaction = {"schema_version": 1, "id": app_id, "owner": owner,
                   "operation": "add_dependency", "source_sha256": digest,
                   "state": "reviewed"}
    event = {"schema_version": 1, "owner": owner, "architecture": "x86",
             "source": "runtime", "requested": "Test runtime", "status": 126,
             "classification": "required_missing"}
    for record in (manifest, transaction, event):
        validator.validate(record)
    bad_generation = deepcopy(manifest)
    bad_generation["owner"]["generation"] = 0
    for invalid in (bad_generation, dict(manifest, architecture="arm"),
                    dict(transaction, operation="global_install"),
                    dict(transaction, kernel_authority=True),
                    dict(event, classification="auto_install"),
                    dict(event, requested="x" * 513)):
        if validator.is_valid(invalid):
            raise ValueError("Invalid record was accepted")
    return {"accepted": 3, "rejected": 6}


def compare(reference, candidate):
    """Report case differences and missing observations without inferring success."""
    expected, actual = reference["cases"], candidate["cases"]
    return [
        {"case": name, "reference": expected.get(name), "candidate": actual.get(name),
         "result": ("unmeasured" if name not in expected or name not in actual
                    else "match" if expected[name] == actual[name] else "difference")}
        for name in sorted(expected.keys() | actual.keys())
    ]


def validate_comparison():
    reference = {"cases": {"same": 1, "changed": 2, "missing": 3}}
    candidate = {"cases": {"same": 1, "changed": 4, "extra": 5}}
    results = {row["case"]: row["result"] for row in compare(reference, candidate)}
    if results != {"same": "match", "changed": "difference",
                   "missing": "unmeasured", "extra": "unmeasured"}:
        raise ValueError("Comparison lost a difference or unmeasured case")
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate", type=Path)
    args = parser.parse_args()
    evidence = ROOT / "evidence/M14/9/windows-host.json"
    reference = read(evidence)
    probe = Path(__file__).with_name("windows_probe.py")
    if reference["probe_sha256"] != hashlib.sha256(probe.read_bytes()).hexdigest():
        raise ValueError("Reference probe hash does not match")
    result = {"record_schema": validate_records(), "reference_cases": len(reference["cases"]),
              "comparison_fixture": validate_comparison()}
    if args.candidate:
        result["comparison"] = compare(reference, read(args.candidate))
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
