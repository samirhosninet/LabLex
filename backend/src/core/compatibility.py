from typing import Dict, Any, List, Tuple

def check_compatibility(manifests: Dict[str, Dict[str, Any]]) -> Tuple[bool, List[str]]:
    """
    Checks compatibility between registered components in a RunSpec composition.
    Returns (compatible, errors_list).
    
    IMPORTANT: This logic is component-agnostic and relies on dynamic checks of available manifests.
    """
    errors = []
    
    tool = manifests.get("external_tool")
    adapter = manifests.get("adapter")
    result_schema = manifests.get("result_schema")
    benchmark = manifests.get("benchmark")
    target = manifests.get("target")
    model = manifests.get("model")
    
    # 1. Tool - Adapter compatibility
    if tool and adapter:
        tool_id = tool.get("id")
        adapter_id = adapter.get("id")
        compatible_adapters = tool.get("compatible_adapters", [])
        if adapter_id not in compatible_adapters:
            errors.append(
                f"Adapter '{adapter_id}' is not compatible with ExternalTool '{tool_id}'. "
                f"Compatible adapters: {compatible_adapters}."
            )
            
    # 2. Adapter - ResultSchema compatibility
    if adapter and result_schema:
        adapter_id = adapter.get("id")
        schema_id = result_schema.get("id")
        compatible_schemas = adapter.get("compatible_result_schemas", [])
        if schema_id not in compatible_schemas:
            errors.append(
                f"ResultSchema '{schema_id}' is not compatible with Adapter '{adapter_id}'. "
                f"Compatible schemas: {compatible_schemas}."
            )
            
    # 3. Model - Target compatibility
    if model and target:
        model_id = model.get("id")
        target_id = target.get("id")
        model_provider = model.get("provider_id")
        target_provider = target.get("provider_id")
        compatible_targets = model.get("compatible_targets", [])
        
        # Check provider matching
        if model_provider != target_provider:
            errors.append(
                f"Model provider '{model_provider}' does not match Target provider '{target_provider}'."
            )
            
        # Check target specific compatibility if compatible_targets is declared and not empty
        if compatible_targets and target_id not in compatible_targets:
            errors.append(
                f"Target '{target_id}' is not listed as compatible for Model '{model_id}'. "
                f"Compatible targets: {compatible_targets}."
            )
            
    # 4. Benchmark - ResultSchema compatibility (Metrics validation)
    if benchmark and result_schema:
        benchmark_id = benchmark.get("id")
        schema_id = result_schema.get("id")
        required_metrics = benchmark.get("required_metrics", [])
        extraction_rules = result_schema.get("extraction_rules", {})
        extracted_metrics = list(extraction_rules.get("metrics", {}).keys())
        
        missing_metrics = [m for m in required_metrics if m not in extracted_metrics]
        if missing_metrics:
            errors.append(
                f"ResultSchema '{schema_id}' is missing JSONPath extraction rules for benchmark required metrics: {missing_metrics}."
            )
            
    # 5. Tool - Benchmark compatibility (optional constraint)
    if tool and benchmark:
        supported_benchmarks = tool.get("supported_benchmarks")
        benchmark_id = benchmark.get("id")
        if supported_benchmarks is not None and benchmark_id not in supported_benchmarks:
            errors.append(
                f"Benchmark '{benchmark_id}' is not supported by ExternalTool '{tool.get('id')}'. "
                f"Supported benchmarks: {supported_benchmarks}."
            )
            
    return len(errors) == 0, errors
