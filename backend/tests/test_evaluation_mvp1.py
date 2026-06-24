import pytest
from src.core.validators import validate_manifest
from src.core.compatibility import check_compatibility
from src.core.normalizer import normalize_result_data
from src.core.errors import LabLexException

def test_manifest_validation():
    # Valid external_tool manifest payload
    valid_tool = {
        "kind": "external_tool",
        "id": "mock_tool",
        "name": "Mock Evaluation Tool",
        "schema_version": "1.0",
        "manifest_version": "1.0.0",
        "endpoint": "http://localhost:8080/eval",
        "compatible_adapters": ["mock_adapter_v1"]
    }
    # Validates correctly without throwing errors
    validate_manifest("external_tool", valid_tool)
    
    # Invalid external_tool manifest payload (missing endpoint)
    invalid_tool = {
        "kind": "external_tool",
        "id": "mock_tool",
        "name": "Mock Evaluation Tool",
        "schema_version": "1.0",
        "manifest_version": "1.0.0",
        "compatible_adapters": ["mock_adapter_v1"]
    }
    with pytest.raises(LabLexException) as excinfo:
        validate_manifest("external_tool", invalid_tool)
    assert excinfo.value.code == "VALIDATION_ERROR"
    assert any("endpoint" in msg for msg in excinfo.value.details.values())

def test_compatibility_engine():
    # 1. Define fully compatible components manifest dictionary
    manifests = {
        "external_tool": {
            "id": "mock_tool",
            "compatible_adapters": ["mock_adapter_v1"]
        },
        "adapter": {
            "id": "mock_adapter_v1",
            "compatible_result_schemas": ["schema_v1"]
        },
        "result_schema": {
            "id": "schema_v1",
            "extraction_rules": {
                "sample_path": "$.results",
                "sample_id": "$.id",
                "output_text": "$.output",
                "metrics": {
                    "accuracy": "$.metrics.accuracy",
                    "latency": "$.latency_ms"
                }
            }
        },
        "benchmark": {
            "id": "benchmark_v1",
            "required_metrics": ["accuracy"]
        },
        "target": {
            "id": "target_v1",
            "provider_id": "openai"
        },
        "model": {
            "id": "model_v1",
            "provider_id": "openai"
        }
    }
    
    compatible, errors = check_compatibility(manifests)
    assert compatible is True
    assert len(errors) == 0
    
    # 2. Check compatibility failure with wrong adapter ID
    manifests_bad_adapter = manifests.copy()
    manifests_bad_adapter["adapter"] = {
        "id": "wrong_adapter_id",
        "compatible_result_schemas": ["schema_v1"]
    }
    compatible, errors = check_compatibility(manifests_bad_adapter)
    assert compatible is False
    assert any("Adapter" in e for e in errors)
    
    # 3. Check compatibility failure with mismatched provider ID
    manifests_bad_provider = manifests.copy()
    manifests_bad_provider["target"] = {
        "id": "target_v1",
        "provider_id": "anthropic"
    }
    compatible, errors = check_compatibility(manifests_bad_provider)
    assert compatible is False
    assert any("provider" in e.lower() for e in errors)

def test_jsonpath_normalizer():
    # Simulated raw output
    raw_data = {
        "results": [
            {
                "id": "c1",
                "input": "User query 1",
                "expected": "Response 1",
                "actual": "Model response 1",
                "latency_ms": 100,
                "metrics": {
                    "accuracy": 1.0
                }
            },
            {
                "id": "c2",
                "input": "User query 2",
                "expected": "Response 2",
                "actual": "Model response 2",
                "latency_ms": 200,
                "metrics": {
                    "accuracy": 0.8
                }
            }
        ]
    }
    
    # ResultSchema rules definition
    result_schema = {
        "extraction_rules": {
            "sample_path": "$.results",
            "sample_id": "$.id",
            "input_text": "$.input",
            "expected_output": "$.expected",
            "output_text": "$.actual",
            "latency_ms": "$.latency_ms",
            "metrics": {
                "accuracy": "$.metrics.accuracy"
            }
        }
    }
    
    samples, summary = normalize_result_data(raw_data, result_schema)
    assert len(samples) == 2
    
    # Assert sample 1 mapping
    assert samples[0]["sample_id"] == "c1"
    assert samples[0]["input_text"] == "User query 1"
    assert samples[0]["expected_output"] == "Response 1"
    assert samples[0]["output_text"] == "Model response 1"
    assert samples[0]["latency_ms"] == 100
    assert samples[0]["metrics"]["accuracy"] == 1.0
    assert samples[0]["status"] == "completed"
    
    # Assert summary metrics calculations
    assert summary["total_samples"] == 2
    assert summary["completed_count"] == 2
    assert summary["failed_count"] == 0
    assert summary["average_latency_ms"] == 150.0
    assert summary["average_accuracy"] == 0.90
