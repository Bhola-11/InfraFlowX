"""
Domain Validation Rules & Data Integrity Checks for Facilities
"""
import re
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class FacilitiesValidator:
    """
    Enterprise business rules, regulatory thresholds, and format validators for facilities.
    """
    @staticmethod
    def validate_code_format(code_str, prefix="FAC"):
        if not code_str:
            raise ValidationError(_("Code identifier cannot be empty."))
        pattern = rf"^{prefix}-[A-Z0-9_-]+$"
        if not re.match(pattern, code_str):
            raise ValidationError(
                _(f"Identifier '{code_str}' does not conform to required standard format '{prefix}-XXXX'."),
                params={'code': code_str}
            )
        return True

    @staticmethod
    def validate_positive_decimal(value, field_name="Amount"):
        if value is None or Decimal(str(value)) < Decimal('0.00'):
            raise ValidationError(_(f"{field_name} must be a non-negative decimal number."))
        return True

    @staticmethod
    def validate_percentage(value, field_name="Percentage"):
        val = Decimal(str(value))
        if val < Decimal('0.00') or val > Decimal('100.00'):
            raise ValidationError(_(f"{field_name} must be within range 0.00% to 100.00%."))
        return True

    @staticmethod
    def validate_date_sequence(start_date, end_date, start_label="Start Date", end_label="End Date"):
        if start_date and end_date and start_date > end_date:
            raise ValidationError(_(f"{start_label} ({start_date}) cannot be after {end_label} ({end_date})."))
        return True

    @staticmethod
    def validate_score_range(score, min_val=0, max_val=100, field_name="Score"):
        if score < min_val or score > max_val:
            raise ValidationError(_(f"{field_name} ({score}) must be between {min_val} and {max_val}."))
        return True
