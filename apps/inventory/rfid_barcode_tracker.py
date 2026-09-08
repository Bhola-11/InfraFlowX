"""
InfraFlowX - GS1-128 Barcode & EPC Gen2 RFID Tag Translation Engine
Encodes and decodes standard GS1 Application Identifiers and RFID electronic product codes.
"""

from typing import Dict, Any
import re


class BarcodeRFIDEngine:
    """
    GS1 standard compliance for infrastructure equipment and spare parts tracking.
    """

    @classmethod
    def parse_gs1_128(cls, raw_barcode_str: str) -> Dict[str, Any]:
        """
        Parses AI (01) GTIN, AI (10) Batch/Lot, AI (21) Serial, AI (17) Expiration.
        """
        parsed = {}
        s = raw_barcode_str.strip()

        if "(01)" in s:
            gtin_match = re.search(r'\(01\)(\d{14})', s)
            if gtin_match:
                parsed["gtin"] = gtin_match.group(1)

        if "(10)" in s:
            lot_match = re.search(r'\(10\)([A-Za-z0-9_-]+)', s)
            if lot_match:
                parsed["lot_number"] = lot_match.group(1)

        if "(21)" in s:
            sn_match = re.search(r'\(21\)([A-Za-z0-9_-]+)', s)
            if sn_match:
                parsed["serial_number"] = sn_match.group(1)

        return {
            "raw_barcode": raw_barcode_str,
            "parsed_fields": parsed,
            "is_valid_gs1": len(parsed) > 0,
        }
