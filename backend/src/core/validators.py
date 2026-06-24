import os
import json
from jsonschema import Draft202012Validator
from src.core.errors import LabLexException

SCHEMA_DIR = os.path.realpath(os.path.join(os.path.dirname(os.path.dirname(__file__)), "schemas", "manifests"))
_schemas = {}

def load_schemas():
    global _schemas
    if not os.path.exists(SCHEMA_DIR):
        return
    for filename in os.listdir(SCHEMA_DIR):
        if filename.endswith(".json"):
            path = os.path.join(SCHEMA_DIR, filename)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    schema_data = json.load(f)
                    key = filename.split(".json")[0]
                    _schemas[key] = schema_data
                    
                    # Also map just the kind, if defined in properties
                    if "properties" in schema_data and "kind" in schema_data["properties"]:
                        kind_prop = schema_data["properties"]["kind"]
                        if "const" in kind_prop:
                            kind = kind_prop["const"]
                            _schemas[kind] = schema_data
            except Exception as e:
                # Silently skip schemas that fail to parse during startup
                pass

def validate_manifest(kind: str, data: dict, version: str = "v1"):
    """
    Validates manifest data against JSON Schema.
    Raises LabLexException if validation fails.
    """
    schema_key = f"{kind}_{version}"
    if schema_key not in _schemas:
        schema_key = kind
        
    if schema_key not in _schemas:
        raise LabLexException(
            code="SCHEMA_NOT_FOUND",
            message=f"Schema for kind '{kind}' and version '{version}' was not found.",
            status_code=400
        )
        
    schema = _schemas[schema_key]
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(data), key=lambda e: e.path)
    
    if errors:
        details = {}
        for error in errors:
            path = ".".join([str(p) for p in error.path]) if error.path else "root"
            details[path] = error.message
            
        raise LabLexException(
            code="VALIDATION_ERROR",
            message="Manifest schema validation failed.",
            status_code=400,
            details=details
        )

# Load schemas on startup
load_schemas()
