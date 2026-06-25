from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from src.models.evaluation import ToolRun, NormalizedResult, NormalizedSample
from src.core.errors import LabLexException

def is_lower_better(metric_name: str) -> bool:
    """
    Heuristic to determine if a lower value is better for a given metric.
    """
    lower_better_keywords = ["latency", "cost", "error", "time", "ms", "duration", "loss"]
    name_lower = metric_name.lower()
    return any(kw in name_lower for kw in lower_better_keywords)

def calculate_comparison(run_id_a: str, run_id_b: str, db: Session) -> Dict[str, Any]:
    """
    Compares two ToolRuns side by side:
    - Matches samples by sample_id
    - Calculates delta (B - A) for each metric
    - Highlights winners per metric (both sample-level and overall)
    """
    # Fetch runs
    run_a = db.query(ToolRun).filter(ToolRun.id == run_id_a).first()
    run_b = db.query(ToolRun).filter(ToolRun.id == run_id_b).first()

    if not run_a or not run_b:
        raise LabLexException(
            code="NOT_FOUND",
            message="One or both runs to compare could not be found.",
            status_code=404
        )

    if run_a.status != "completed" or run_b.status != "completed":
        raise LabLexException(
            code="INVALID_STATE",
            message="Runs must be fully completed before performing a comparison.",
            status_code=400
        )

    norm_a: Optional[NormalizedResult] = run_a.normalized_results[0] if run_a.normalized_results else None
    norm_b: Optional[NormalizedResult] = run_b.normalized_results[0] if run_b.normalized_results else None

    if not norm_a or not norm_b:
        raise LabLexException(
            code="INVALID_STATE",
            message="Missing normalized results for one or both runs.",
            status_code=400
        )

    # Index samples by sample_id
    samples_a: Dict[str, NormalizedSample] = {s.sample_id: s for s in norm_a.samples}
    samples_b: Dict[str, NormalizedSample] = {s.sample_id: s for s in norm_b.samples}

    all_sample_ids = sorted(list(set(samples_a.keys()) | set(samples_b.keys())))

    compared_samples: List[Dict[str, Any]] = []

    # Keep track of aggregated deltas
    metrics_summary_a = norm_a.metrics_summary or {}
    metrics_summary_b = norm_b.metrics_summary or {}
    
    # Calculate sample-level comparison
    for sid in all_sample_ids:
        sa = samples_a.get(sid)
        sb = samples_b.get(sid)

        sample_comparison = {
            "sample_id": sid,
            "run_a": {
                "status": sa.status if sa else "missing",
                "output_text": sa.output_text if sa else None,
                "latency_ms": sa.latency_ms if sa else None,
                "metrics": sa.metrics if sa else {}
            },
            "run_b": {
                "status": sb.status if sb else "missing",
                "output_text": sb.output_text if sb else None,
                "latency_ms": sb.latency_ms if sb else None,
                "metrics": sb.metrics if sb else {}
            },
            "metrics_comparison": {}
        }

        # Compare metrics
        metrics_a = sa.metrics if sa else {}
        metrics_b = sb.metrics if sb else {}
        all_metrics_keys = set(metrics_a.keys()) | set(metrics_b.keys())

        # Include latency_ms as a standard metric if available
        if (sa and sa.latency_ms is not None) or (sb and sb.latency_ms is not None):
            metrics_a = {**metrics_a, "latency_ms": sa.latency_ms} if sa else metrics_a
            metrics_b = {**metrics_b, "latency_ms": sb.latency_ms} if sb else metrics_b
            all_metrics_keys.add("latency_ms")

        for mkey in all_metrics_keys:
            val_a = metrics_a.get(mkey)
            val_b = metrics_b.get(mkey)

            if val_a is not None and val_b is not None:
                try:
                    val_a_f = float(val_a)
                    val_b_f = float(val_b)
                    delta = val_b_f - val_a_f
                    lower_better = is_lower_better(mkey)

                    # Determine winner
                    if delta == 0:
                        winner = "draw"
                    elif (delta > 0 and not lower_better) or (delta < 0 and lower_better):
                        winner = "run_b"
                    else:
                        winner = "run_a"

                    sample_comparison["metrics_comparison"][mkey] = {
                        "val_a": val_a_f,
                        "val_b": val_b_f,
                        "delta": round(delta, 4),
                        "winner": winner
                    }
                except ValueError:
                    sample_comparison["metrics_comparison"][mkey] = {
                        "val_a": val_a,
                        "val_b": val_b,
                        "delta": None,
                        "winner": "incomparable"
                    }

        compared_samples.append(sample_comparison)

    # Calculate run-level summary comparison
    summary_comparison: Dict[str, Any] = {}
    all_summary_keys = set(metrics_summary_a.keys()) | set(metrics_summary_b.keys())
    
    # Also add average latency if present
    if "average_latency_ms" in metrics_summary_a or "average_latency_ms" in metrics_summary_b:
        all_summary_keys.add("average_latency_ms")

    for skey in all_summary_keys:
        val_a = metrics_summary_a.get(skey)
        val_b = metrics_summary_b.get(skey)

        if val_a is not None and val_b is not None:
            try:
                val_a_f = float(val_a)
                val_b_f = float(val_b)
                delta = val_b_f - val_a_f
                lower_better = is_lower_better(skey)

                if delta == 0:
                    winner = "draw"
                elif (delta > 0 and not lower_better) or (delta < 0 and lower_better):
                    winner = "run_b"
                else:
                    winner = "run_a"

                summary_comparison[skey] = {
                    "val_a": val_a_f,
                    "val_b": val_b_f,
                    "delta": round(delta, 4),
                    "winner": winner
                }
            except ValueError:
                summary_comparison[skey] = {
                    "val_a": val_a,
                    "val_b": val_b,
                    "delta": None,
                    "winner": "incomparable"
                }

    # Decide overall run winner based on metric votes
    votes = {"run_a": 0, "run_b": 0, "draw": 0}
    for item in summary_comparison.values():
        winner = item.get("winner")
        if winner in votes:
            votes[winner] += 1

    overall_winner = "draw"
    if votes["run_a"] > votes["run_b"]:
        overall_winner = "run_a"
    elif votes["run_b"] > votes["run_a"]:
        overall_winner = "run_b"

    return {
        "run_a": {
            "id": run_a.id,
            "created_at": run_a.created_at,
            "runspec_components": run_a.runspec.components if run_a.runspec else {}
        },
        "run_b": {
            "id": run_b.id,
            "created_at": run_b.created_at,
            "runspec_components": run_b.runspec.components if run_b.runspec else {}
        },
        "summary": summary_comparison,
        "overall_winner": overall_winner,
        "samples": compared_samples
    }
