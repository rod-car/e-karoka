from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required, permission_required

from ..models import DocumentType
from ..forms import DocumentTypeForm

from django.db import transaction
from django.contrib import messages

@permission_required(perm="manage-document_type", login_url="/login", raise_exception=True)
def create(request: HttpRequest):
    if (request.method == "POST"):
        form = DocumentTypeForm(request.POST)
        if (form.is_valid()):
            label = form.cleaned_data['label']
            description = form.cleaned_data['description']
            
            document_type = DocumentType(
                label = label,
                description = description
            )
            
            transaction.set_autocommit(False)
            document_type.save()
            transaction.commit()
            transaction.set_autocommit(True)
            messages.success(request=request, message="Succès")
            
            return redirect(to="client:document-type-create", permanent=True)
    
    form = DocumentTypeForm()
    return render(request=request, template_name="client/document_type/new.html", context={
        "form": form
    })

@permission_required(perm="manage-document_type", login_url="/login", raise_exception=True)
def list(request: HttpRequest):
    type_documents = DocumentType.objects.all()
    
    return render(request=request, template_name="client/document_type/list.html", context={
        "type_documents": type_documents
    })

@permission_required(perm="manage-document_type", login_url="/login", raise_exception=True)
def edit(request: HttpRequest, id: int):
    document_type = get_object_or_404(klass=DocumentType, pk=id)
    form = DocumentTypeForm(instance=document_type)
    
    if (request.method == "POST"):
        form = DocumentTypeForm(request.POST, instance=document_type)
        if (form.is_valid()):
            form.save(commit=True)

            return redirect(to="client:document-type-list", permanent=True)
    
    return render(request=request, template_name="client/document_type/edit.html", context={
        "document_type": document_type,
        "form": form
    })

@permission_required(perm="manage-document_type", login_url="/login", raise_exception=True)
def delete(request: HttpRequest):
    if (request.method == "GET"): raise Exception("Get method not supported for this route")
    
    id = request.POST['id']
    document_type = get_object_or_404(klass=DocumentType, pk=id)
    document_type.delete()
    return redirect("client:document-type-list")