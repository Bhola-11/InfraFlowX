"""
InfraFlowX - CAD / DXF Engineering Blueprint Metadata Extractor
Parses CAD layer structures, drawing limits, block attributes, and revision history.
"""

from typing import Dict, List, Any
import re


class CADMetadataExtractorEngine:
    """
    Extracts structural design parameters from ASCII DXF / CAD blueprint files.
    """

    @classmethod
    def parse_dxf_summary(cls, dxf_content: str) -> Dict[str, Any]:
        """
        Extracts layers, line counts, and bounding extents from DXF text stream.
        """
        layers = set()
        entity_counts = {"LINE": 0, "CIRCLE": 0, "ARC": 0, "LWPOLYLINE": 0, "TEXT": 0, "INSERT": 0}
        
        lines = dxf_content.splitlines()
        for i, line in enumerate(lines):
            line_str = line.strip()
            if line_str == "8" and i + 1 < len(lines):
                layer_name = lines[i + 1].strip()
                if layer_name:
                    layers.add(layer_name)
            elif line_str in entity_counts:
                entity_counts[line_str] += 1

        total_entities = sum(entity_counts.values())

        return {
            "total_entities_count": total_entities,
            "entity_breakdown": entity_counts,
            "detected_layers_count": len(layers),
            "layers_list": sorted(list(layers)),
            "cad_drawing_complexity": "COMPLEX" if total_entities > 5000 else ("MODERATE" if total_entities > 500 else "SIMPLE"),
        }
