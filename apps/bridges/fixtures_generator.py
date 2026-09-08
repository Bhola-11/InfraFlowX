"""
InfraFlowX - Realistic Mock Fixtures & Synthetic Data Generator for Bridges
Generates randomized, mathematically sound domain test fixtures for benchmarking.
"""

from typing import List, Dict, Any
import random
from datetime import datetime, timedelta


class BridgesFixtureGenerator:
    """
    Generates synthetic realistic records for bridges.
    """

    @classmethod
    def generate_synthetic_records(cls, count: int = 50) -> List[Dict[str, Any]]:
        records = []
        now = datetime.now()
        
        statuses = ["ACTIVE", "PENDING", "MAINTENANCE_REQUIRED", "OPERATIONAL", "UNDER_REVIEW"]

        for i in range(1, count + 1):
            created_delta = timedelta(days=random.randint(1, 365))
            rec = {
                "id": i,
                "name": f"Bridges Synthetic Asset #{i:04d}",
                "code": f"IFX-BRI-{i:05d}",
                "status": random.choice(statuses),
                "condition_score": random.randint(45, 100),
                "created_at": (now - created_delta).isoformat(),
                "latitude": round(37.7749 + random.uniform(-0.15, 0.15), 6),
                "longitude": round(-122.4194 + random.uniform(-0.15, 0.15), 6),
                "cost_usd": round(random.uniform(5000.0, 500000.0), 2),
            }
            records.append(rec)

        return records
