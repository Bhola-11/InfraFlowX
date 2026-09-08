"""
Contractor Serializers
"""
from apps.contractors.models import Contractor, ContractAgreement, ContractorEvaluation


class ContractorSerializer:
    @staticmethod
    def to_dict(c):
        return {
            'id': str(c.id),
            'company_name': c.company_name,
            'registration_number': c.registration_number,
            'contact_person': c.contact_person,
            'email': c.email,
            'phone': c.phone,
            'specialization': c.specialization,
            'specialization_display': c.get_specialization_display(),
            'rating': float(c.rating),
            'status': c.status,
            'status_display': c.get_status_display(),
            'agreements_count': c.agreements.count(),
        }
