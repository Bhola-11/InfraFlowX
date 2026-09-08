from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from .models import DocumentCategory, Document, DocumentVersion, BlueprintMetadata
from .forms import DocumentCategoryForm, DocumentForm, DocumentVersionForm, BlueprintMetadataForm
from apps.audit.utils import log_audit_event


@login_required
def document_list_view(request):
    docs = Document.objects.select_related('category', 'asset', 'project', 'organization', 'uploaded_by').all()
    q = request.GET.get('q', '').strip()
    cat_id = request.GET.get('category', '').strip()
    status = request.GET.get('status', '').strip()
    conf = request.GET.get('confidentiality', '').strip()
    is_bp = request.GET.get('is_blueprint', '').strip()

    if q:
        docs = docs.filter(Q(title__icontains=q) | Q(doc_number__icontains=q) | Q(tags__icontains=q))
    if cat_id:
        docs = docs.filter(category_id=cat_id)
    if status:
        docs = docs.filter(status=status)
    if conf:
        docs = docs.filter(confidentiality=conf)
    if is_bp:
        docs = docs.filter(is_blueprint=(is_bp.lower() == 'true' or is_bp == '1'))

    paginator = Paginator(docs, 20)
    page_obj = paginator.get_page(request.GET.get('page'))
    categories = DocumentCategory.objects.all()

    return render(request, 'documents/document_list.html', {
        'page_obj': page_obj,
        'categories': categories,
        'search_query': q,
        'selected_cat': cat_id,
        'selected_status': status,
        'selected_conf': conf,
        'is_bp_filter': is_bp,
        'total_docs': docs.count(),
    })


@login_required
def blueprint_list_view(request):
    blueprints = Document.objects.filter(is_blueprint=True).select_related('category', 'asset', 'project', 'blueprint_info')
    q = request.GET.get('q', '').strip()
    if q:
        blueprints = blueprints.filter(Q(title__icontains=q) | Q(doc_number__icontains=q) | Q(blueprint_info__drawing_number__icontains=q))

    paginator = Paginator(blueprints, 15)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'documents/blueprint_list.html', {
        'page_obj': page_obj,
        'search_query': q,
        'total_blueprints': blueprints.count(),
    })


@login_required
def document_detail_view(request, pk):
    doc = get_object_or_404(Document.objects.select_related('category', 'asset', 'project', 'organization', 'uploaded_by'), pk=pk)
    versions = doc.versions.select_related('uploaded_by').all()
    version_form = DocumentVersionForm()
    blueprint_form = BlueprintMetadataForm(instance=getattr(doc, 'blueprint_info', None)) if doc.is_blueprint else None

    return render(request, 'documents/document_detail.html', {
        'doc': doc,
        'versions': versions,
        'version_form': version_form,
        'blueprint_form': blueprint_form,
    })


@login_required
def document_create_view(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.uploaded_by = request.user
            if request.FILES.get('file'):
                doc.file_size_bytes = request.FILES['file'].size
                doc.mime_type = request.FILES['file'].content_type
            doc.save()
            log_audit_event(request.user, 'CREATE', 'Document', str(doc.id), f"Uploaded document {doc.title} ({doc.doc_number})")
            messages.success(request, f"Document '{doc.title}' uploaded successfully.")
            return redirect('documents:document_detail', pk=doc.id)
    else:
        init_num = f"DOC-{timezone.now().strftime('%Y%m%d%H%M')}"
        form = DocumentForm(initial={'doc_number': init_num, 'uploaded_by': request.user})
    return render(request, 'documents/document_form.html', {'form': form, 'title': 'Upload Engineering Document / Asset Record'})


@login_required
def document_update_view(request, pk):
    doc = get_object_or_404(Document, pk=pk)
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES, instance=doc)
        if form.is_valid():
            doc = form.save(commit=False)
            if request.FILES.get('file'):
                doc.file_size_bytes = request.FILES['file'].size
                doc.mime_type = request.FILES['file'].content_type
            doc.save()
            log_audit_event(request.user, 'UPDATE', 'Document', str(doc.id), f"Updated document metadata {doc.title}")
            messages.success(request, f"Document '{doc.title}' updated.")
            return redirect('documents:document_detail', pk=doc.id)
    else:
        form = DocumentForm(instance=doc)
    return render(request, 'documents/document_form.html', {'form': form, 'title': f'Edit Document - {doc.title}', 'doc': doc})


@login_required
def document_version_create_view(request, pk):
    doc = get_object_or_404(Document, pk=pk)
    if request.method == 'POST':
        form = DocumentVersionForm(request.POST, request.FILES)
        if form.is_valid():
            v = form.save(commit=False)
            v.document = doc
            v.uploaded_by = request.user
            v.save()
            doc.current_version = v.version_number
            if v.file:
                doc.file = v.file
                doc.file_size_bytes = v.file.size
            doc.save()
            log_audit_event(request.user, 'CREATE', 'DocumentVersion', str(v.id), f"Added version {v.version_number} to {doc.title}")
            messages.success(request, f"New version v{v.version_number} added.")
    return redirect('documents:document_detail', pk=doc.id)


@login_required
def category_list_view(request):
    cats = DocumentCategory.objects.all()
    form = DocumentCategoryForm()
    if request.method == 'POST':
        form = DocumentCategoryForm(request.POST)
        if form.is_valid():
            cat = form.save()
            log_audit_event(request.user, 'CREATE', 'DocumentCategory', str(cat.id), f"Created category {cat.name}")
            messages.success(request, f"Category '{cat.name}' created.")
            return redirect('documents:category_list')
    return render(request, 'documents/category_list.html', {'categories': cats, 'form': form})
