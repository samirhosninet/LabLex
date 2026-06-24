from jsonpath_ng import parse
from typing import Dict, Any, List, Tuple

def normalize_result_data(raw_data: Dict[str, Any], result_schema: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    """
    Parses raw evaluation results using JSONPath rules defined in the ResultSchema manifest.
    
    Args:
        raw_data (dict): The captured raw output from the adapter.
        result_schema (dict): The result schema manifest mapping raw fields to standardized fields.
        
    Returns:
        tuple: (normalized_samples_list, metrics_summary_dict)
    """
    extraction_rules = result_schema.get("extraction_rules", {})
    sample_path = extraction_rules.get("sample_path", "$.results")
    
    # 1. Locate samples list
    sample_expr = parse(sample_path)
    sample_matches = sample_expr.find(raw_data)
    
    if not sample_matches:
        raise ValueError(f"No samples array found at JSONPath: '{sample_path}'")
        
    raw_samples = sample_matches[0].value
    if not isinstance(raw_samples, list):
        raise ValueError(f"Object found at JSONPath '{sample_path}' is not a list.")
        
    # Extract rules paths
    id_rule = extraction_rules.get("sample_id", "$.id")
    input_rule = extraction_rules.get("input_text", "$.input")
    expected_rule = extraction_rules.get("expected_output", "$.expected")
    output_rule = extraction_rules.get("output_text", "$.actual")
    error_rule = extraction_rules.get("error_message", "$.error")
    latency_rule = extraction_rules.get("latency_ms", "$.latency_ms")
    metrics_rules = extraction_rules.get("metrics", {})
    
    # Compile JSONPath expressions
    id_expr = parse(id_rule)
    input_expr = parse(input_rule) if input_rule else None
    expected_expr = parse(expected_rule) if expected_rule else None
    output_expr = parse(output_rule)
    error_expr = parse(error_rule) if error_rule else None
    latency_expr = parse(latency_rule) if latency_rule else None
    
    parsed_metrics_exprs = {k: parse(v) for k, v in metrics_rules.items()}
    
    normalized_samples = []
    
    # Stats accumulation
    total_latency = 0
    completed_count = 0
    failed_count = 0
    metric_sums = {k: 0.0 for k in metrics_rules.keys()}
    
    for idx, raw_sample in enumerate(raw_samples):
        # Extract Sample ID
        id_match = id_expr.find(raw_sample)
        sample_id = str(id_match[0].value) if id_match else f"sample_{idx}"
        
        # Extract fields
        input_match = input_expr.find(raw_sample) if input_expr else None
        input_val = input_match[0].value if input_match else None
        
        expected_match = expected_expr.find(raw_sample) if expected_expr else None
        expected_val = expected_match[0].value if expected_match else None
        
        output_match = output_expr.find(raw_sample)
        output_val = output_match[0].value if output_match else None
        
        error_match = error_expr.find(raw_sample) if error_expr else None
        error_val = error_match[0].value if error_match else None
        
        latency_match = latency_expr.find(raw_sample) if latency_expr else None
        latency_val = int(latency_match[0].value) if latency_match else None
        
        # Extract metrics
        sample_metrics = {}
        for metric_name, expr in parsed_metrics_exprs.items():
            metric_match = expr.find(raw_sample)
            if metric_match:
                val = metric_match[0].value
                try:
                    val_float = float(val)
                    sample_metrics[metric_name] = val_float
                    metric_sums[metric_name] += val_float
                except (ValueError, TypeError):
                    sample_metrics[metric_name] = 0.0
            else:
                sample_metrics[metric_name] = 0.0
                
        # Determine status
        status = "completed"
        if error_val or output_val is None:
            status = "failed"
            failed_count += 1
        else:
            completed_count += 1
            
        if latency_val:
            total_latency += latency_val
            
        normalized_samples.append({
            "sample_id": sample_id,
            "input_text": input_val,
            "expected_output": expected_val,
            "output_text": output_val,
            "error_message": error_val,
            "latency_ms": latency_val,
            "metrics": sample_metrics,
            "status": status
        })
        
    # Build statistics summary
    total_samples = len(raw_samples)
    avg_latency = total_latency / total_samples if total_samples > 0 else 0
    
    metrics_summary = {
        "total_samples": total_samples,
        "completed_count": completed_count,
        "failed_count": failed_count,
        "average_latency_ms": round(avg_latency, 2),
    }
    
    for metric_name, m_sum in metric_sums.items():
        metrics_summary[f"average_{metric_name}"] = round(m_sum / total_samples, 4) if total_samples > 0 else 0.0
        
    return normalized_samples, metrics_summary
