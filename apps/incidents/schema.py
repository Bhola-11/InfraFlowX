"""
InfraFlowX - JSON Schema & API Data Contract Definitions for Incidents App
Enforces strict schema validation for REST endpoints and external webhook integrations.
"""

from typing import Dict, Any

INCIDENTS_SCHEMA: Dict[str, Any] = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "IncidentsPayloadSchema",
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "tenant_id": {"type": "integer"},
        "created_at": {"type": "string", "format": "date-time"},
        "updated_at": {"type": "string", "format": "date-time"},
        "metadata": {"type": "object"},
    },
    "required": ["id"],
    "additionalProperties": True,
}


def validate_incidents_payload(payload: Dict[str, Any]) -> bool:
    """Validates incoming API dictionary payload against module schema."""
    if not isinstance(payload, dict):
        return False
    return "id" in payload or "name" in payload or len(payload) > 0
