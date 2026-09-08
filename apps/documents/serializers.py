"""
Document Serializers
"""
from apps.documents.models import Document, BlueprintMetadata


class DocumentSerializer:
    @staticmethod
    def to_dict(doc):
        return {
            'id': str(doc.id),
            'doc_number': doc.doc_number,
            'title': doc.title,
            'category': doc.category.name if doc.category else None,
            'current_version': doc.current_version,
            'is_blueprint': doc.is_blueprint,
            'confidentiality': doc.confidentiality,
            'status': doc.status,
            'uploaded_by': doc.uploaded_by.get_full_name() if doc.uploaded_by else None,
            'created_at': doc.created_at.isoformat() if doc.created_at else None,
        }
