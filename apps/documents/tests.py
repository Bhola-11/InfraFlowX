"""
Comprehensive Unit Tests for Documents App
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.organizations.models import Organization
from apps.documents.models import DocumentCategory, Document, BlueprintMetadata
from apps.documents.services import DocumentService

User = get_user_model()


class DocumentsTestSuite(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='cad_engineer', password='password123')
        self.org = Organization.objects.create(name='Design Bureau', code='DB-01')
        self.cat = DocumentCategory.objects.create(name='Blueprints', code='CAT-DWG')
        self.doc = Document.objects.create(
            doc_number='DWG-TEST-001',
            title='Suspension Cable Anchor Detail',
            category=self.cat,
            organization=self.org,
            current_version='1.0',
            uploaded_by=self.user
        )

    def test_blueprint_metadata(self):
        bp = BlueprintMetadata.objects.create(
            document=self.doc,
            drawing_number='DWG-ANCHOR-01',
            scale_ratio='1:50',
            sheet_size='A0',
            cad_software='AutoCAD 2024'
        )
        self.assertEqual(bp.document, self.doc)
