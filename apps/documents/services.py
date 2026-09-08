"""
Document & CAD Blueprint Management Services
"""
from apps.documents.models import Document, DocumentVersion, BlueprintMetadata
from apps.audit.utils import log_audit_event


class DocumentService:
    @staticmethod
    def register_new_version(document_id, file, version_number, change_log="", user=None):
        doc = Document.objects.get(id=document_id)
        ver = DocumentVersion.objects.create(
            document=doc,
            version_number=version_number,
            file=file,
            change_log=change_log,
            uploaded_by=user
        )
        doc.current_version = version_number
        doc.file = file
        doc.save(update_fields=['current_version', 'file'])
        
        log_audit_event(
            action='DOCUMENT_ACTION',
            module='documents',
            object_id=str(doc.id),
            object_repr=str(doc),
            description=f"New version v{version_number} uploaded for document {doc.doc_number}",
            user=user
        )
        return ver
