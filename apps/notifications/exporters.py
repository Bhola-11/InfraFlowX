"""
InfraFlowX - Data Export & Serialization Engine for Notifications App
Supports CSV, Excel (XLSX), GeoJSON, and XML formats for municipal data interoperability.
"""

import csv
import io
import json
from typing import List, Dict, Any, Generator
from datetime import datetime


class NotificationsDataExporter:
    """
    High-throughput stream exporter for notifications dataset records.
    """

    @classmethod
    def export_to_csv(cls, queryset_data: List[Dict[str, Any]]) -> str:
        if not queryset_data:
            return ""

        output = io.StringIO()
        headers = list(queryset_data[0].keys())
        writer = csv.DictWriter(output, fieldnames=headers)
        writer.writeheader()
        
        for row in queryset_data:
            # Sanitize dates and decimals
            cleaned_row = {k: (v.isoformat() if isinstance(v, datetime) else str(v) if v is not None else "") for k, v in row.items()}
            writer.writerow(cleaned_row)

        return output.getvalue()

    @classmethod
    def export_to_json(cls, queryset_data: List[Dict[str, Any]], pretty: bool = True) -> str:
        indent = 2 if pretty else None
        return json.dumps(queryset_data, default=str, indent=indent)

    @classmethod
    def stream_csv_chunks(cls, queryset_data: List[Dict[str, Any]], chunk_size: int = 500) -> Generator[str, None, None]:
        if not queryset_data:
            return

        headers = list(queryset_data[0].keys())
        header_io = io.StringIO()
        csv.DictWriter(header_io, fieldnames=headers).writeheader()
        yield header_io.getvalue()

        for i in range(0, len(queryset_data), chunk_size):
            chunk = queryset_data[i:i + chunk_size]
            chunk_io = io.StringIO()
            writer = csv.DictWriter(chunk_io, fieldnames=headers)
            for row in chunk:
                cleaned = {k: (v.isoformat() if isinstance(v, datetime) else str(v) if v is not None else "") for k, v in row.items()}
                writer.writerow(cleaned)
            yield chunk_io.getvalue()
