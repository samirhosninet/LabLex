import time
import random
from typing import Dict, Any
from src.adapters.base import BaseAdapter

class MockAdapter(BaseAdapter):
    """
    Mock adapter that simulates running evaluations and generating synthetic
    outputs for control plane verification.
    """
    
    def execute(self, runspec_snapshot: dict, target_snapshot: dict) -> dict:
        # Simulate small network/processing delay (1 second)
        time.sleep(1.0)
        
        # Get benchmark parameters from snapshot
        benchmark = runspec_snapshot.get("snapshots", {}).get("benchmark", {})
        size = benchmark.get("size", 5) # Default to 5 samples
        required_metrics = benchmark.get("required_metrics", ["score"])
        
        # Generate synthetic samples
        samples = []
        for i in range(1, size + 1):
            sample_id = f"sample_{i}"
            latency = random.randint(80, 500)
            
            # Simulate occasional failures
            status = "completed"
            error_msg = None
            output_text = f"Synthetic output prediction for sample {i}."
            
            # 15% chance to simulate a single case failure
            if i == size and size > 2:
                status = "failed"
                error_msg = "Mock Adapter simulated target model provider API failure."
                output_text = None
                
            metrics_payload = {}
            for metric in required_metrics:
                if status == "failed":
                    metrics_payload[metric] = 0.0
                elif metric == "accuracy":
                    metrics_payload[metric] = round(random.uniform(0.7, 1.0), 2)
                elif metric == "latency":
                    metrics_payload[metric] = latency
                else: # Generic score or rating
                    metrics_payload[metric] = round(random.uniform(0.65, 1.0), 2)
                    
            samples.append({
                "id": sample_id,
                "input": f"Mock prompt request {i} for evaluating {runspec_snapshot.get('components', {}).get('model', 'model')}.",
                "expected": f"Expected target output for mock case {i}.",
                "actual": output_text,
                "error": error_msg,
                "latency_ms": latency,
                "metrics": metrics_payload,
                "status": status
            })
            
        return {
            "adapter_id": "mock_adapter_v1",
            "timestamp": int(time.time()),
            "status": "completed",
            "results": samples
        }
