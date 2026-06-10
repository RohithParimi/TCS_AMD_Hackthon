"""
Batch-run the full portfolio through the pipeline and save results.

Produces data/results.json — the single source of truth the API and dashboard read.
This is deliberately precomputed: the demo reads this file (instant, reliable) rather
than running 30 live LLM calls on stage. Keep a live single-app run (crew.py) as the
"watch the agents think" moment; use this batch output for the portfolio view.

Also prints an accuracy scorecard against the expected_6r golden labels — your eval metric.

Run locally to verify correctness (slow on CPU, ~2-3 min/app):
    uv run src/run_all.py

Later, run the SAME script inside an AMD GPU window for speed + to capture metrics.
"""

import os
import sys
import json
import time
from datetime import datetime, timezone

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import DATA_PATH, LLM_MODEL  # noqa: E402
from crew import analyze_app  # noqa: E402


def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(os.path.join(root, DATA_PATH)) as f:
        apps = json.load(f)

    results = []
    errors = []
    latencies = []

    print(f"\nRunning {len(apps)} apps through the pipeline with model '{LLM_MODEL}'.")
    print("This is slow on local CPU — let it run.\n")

    for idx, app in enumerate(apps, 1):
        name = app["name"]
        print(f"[{idx}/{len(apps)}] {name} (expected {app.get('expected_6r')}) ... ", end="", flush=True)
        t0 = time.time()
        try:
            r = analyze_app(app)
            dt = round(time.time() - t0, 1)
            latencies.append(dt)
            r["latency_seconds"] = dt
            r["matches_expected"] = (
                r["decision"].upper() == str(r.get("expected_6r") or "").upper()
            )
            results.append(r)
            flag = "MATCH" if r["matches_expected"] else "MISS"
            print(f"{r['decision']}  [{flag}]  ({dt}s)")
        except Exception as e:
            dt = round(time.time() - t0, 1)
            print(f"ERROR after {dt}s: {e}")
            errors.append({"app_id": app["id"], "app_name": name, "error": str(e)})

    matches = sum(1 for r in results if r.get("matches_expected"))
    avg_latency = round(sum(latencies) / len(latencies), 1) if latencies else None

    payload = {
        "meta": {
            "model": LLM_MODEL,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "total_apps": len(apps),
            "succeeded": len(results),
            "failed": len(errors),
            "decisions_matching_expected": matches,
            "accuracy_pct": round(100 * matches / len(results), 1) if results else 0,
            "avg_latency_seconds": avg_latency,
        },
        "results": results,
        "errors": errors,
    }

    out_path = os.path.join(root, "data", "results.json")
    with open(out_path, "w") as f:
        json.dump(payload, f, indent=2)

    # Scorecard
    print("\n" + "=" * 78)
    print("PORTFOLIO SCORECARD")
    print("=" * 78)
    print(f"{'Application':<32}{'Risk':>5}  {'Decision':<12}{'Expected':<12}{'Match':<6}")
    print("-" * 78)
    for r in results:
        print(f"{r['app_name'][:31]:<32}{r['risk_score']:>5}  "
              f"{r['decision']:<12}{str(r.get('expected_6r')):<12}"
              f"{'MATCH' if r['matches_expected'] else 'MISS':<6}")
    print("-" * 78)
    print(f"Decisions matching golden labels: {matches}/{len(results)} "
          f"({payload['meta']['accuracy_pct']}%)")
    if avg_latency:
        print(f"Avg latency per app: {avg_latency}s")
    if errors:
        print(f"\nErrors ({len(errors)}):")
        for e in errors:
            print(f"  - {e['app_name']}: {e['error']}")
    print("=" * 78)
    print(f"\nSaved -> data/results.json")


if __name__ == "__main__":
    main()