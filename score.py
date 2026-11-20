"""Run the development or release panel with a saved implementation."""
import argparse
import importlib.util
import json
from pathlib import Path
from evaluate import score

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("implementation", type=Path, default=Path("candidate.py"), nargs="?")
    parser.add_argument("--dev", action="store_true")
    args = parser.parse_args()
    spec = importlib.util.spec_from_file_location("entry", args.implementation)
    entry = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(entry)
    result = score(entry.admit, 23 if args.dev else 194127, 32//4 if args.dev else 32)
    print(json.dumps(result,sort_keys=True))
    raise SystemExit(0 if result["passed"] else 1)
