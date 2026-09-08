from django.contrib import admin
from .models import DocumentCategory, Document, DocumentVersion, BlueprintMetadata


@admin.register(DocumentCategory)
class DocumentCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'created_at')
    search_fields = ('name', 'code')


class DocumentVersionInline(admin.TabularInline):
    model = DocumentVersion
    extra = 0


class BlueprintMetadataInline(admin.StackedInline):
    model = BlueprintMetadata
    extra = 0


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('doc_number', 'title', 'category', 'asset', 'project', 'current_version', 'is_blueprint', 'confidentiality', 'status', 'created_at')
    search_fields = ('doc_number', 'title', 'tags')
    list_filter = ('category', 'confidentiality', 'status', 'is_blueprint')
    inlines = [DocumentVersionInline, BlueprintMetadataInline]


@admin.register(DocumentVersion)
class DocumentVersionAdmin(admin.ModelAdmin):
    list_display = ('document', 'version_number', 'uploaded_by', 'uploaded_at')


@admin.register(BlueprintMetadata)
class BlueprintMetadataAdmin(admin.ModelAdmin):
    list_display = ('drawing_number', 'document', 'scale_ratio', 'sheet_size', 'engineer_signoff_name')
