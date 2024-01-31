from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest
from django.core.paginator import Paginator
from django.contrib.auth.decorators import permission_required
from django.db import transaction
import os
from django.contrib import messages 

from sklearn.feature_extraction.text import TfidfVectorizer

from ..modules.text_extractor import extract_text, extract_abstract, extract_author, extract_title
from ..modules.tokenizer import tokenize
from ..modules.vectorizer import vectorize
from ..modules.text_processing import preprocess_text
from ..models import Documents, Index, TfidfValues, Categories, DocumentType

from .upload import update_tfidf_vectors
import json, datetime
from ..forms import DocumentForm

@permission_required(perm="manage-documents", login_url="/login", raise_exception=True)
def list(request: HttpRequest):
    documents = Documents.objects.all()
    
    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/static/tmp"
    for f in os.scandir(path): os.remove(f)
    
    if ('page' in request.GET): page_number = request.GET['page']
    else: page_number = 1
        
    if ('perpage' in request.GET):
        per_page = int(request.GET['perpage'])
        if per_page == 0:
            per_page = 10
    else: per_page = 10
    
    paginator = Paginator(object_list=documents, per_page=per_page)
    page_obj = paginator.get_page(number=page_number)
    
    return render(request=request, template_name="client/documents/list.html", context={
        "page_obj": page_obj,
        "page_number": page_number,
        "per_page": per_page,
    })

@permission_required(perm="manage-documents", login_url="/login", raise_exception=True)
def edit(request: HttpRequest, id: int):
    document = get_object_or_404(klass=Documents, pk=id)
    document.presentation_date = document.presentation_date.isoformat()
    
    form = DocumentForm(instance=document)
    
    if (request.method == "POST"):
        form = DocumentForm(request.POST, instance=document)
        if (form.is_valid()):
            form.save(commit=True)
            return redirect(to="client:document-list", permanent=True)
    
    return render(request=request, template_name="client/documents/edit.html", context={
        "document": document,
        "form": form
    })

@permission_required(perm="manage-documents", login_url="/login", raise_exception=True)
def preview(request: HttpRequest, id: int):
    document = get_object_or_404(klass=Documents, pk=id)
    name = document.file_path.replace("client", "")
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = base_dir + name
    
    new_path = "/static/tmp/01.pdf"
    os.system("cp " + file_path + " " + base_dir + new_path)

    return render(request=request, template_name="client/documents/preview.html", context={
        "document": document,
        "path": new_path
    })

@permission_required(perm="manage-documents", login_url="/login", raise_exception=True)
def index(request: HttpRequest, id: int):
    start = datetime.datetime.now()
    end = None
    
    document = get_object_or_404(klass=Documents, pk=id)
    file_path = document.file_path.replace("client", "")
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = base_dir + file_path
    
    content = extract_text(file_path)
    abstract = extract_abstract(file=file_path)
    
    tokens = tokenize(content)
    vectors = vectorize(tokens=tokens)
    
    document.abstract = abstract
    document.content = content
    document.indexed = True # Marquer le cocument comme indexé
    
    transaction.set_autocommit(False) # Commencer la transaction
    
    try:
        document.save()
        document_vector = vectors.toarray()[0]
        
        tfidf_values = TfidfValues(
            tfidf_vectors = json.dumps(document_vector.tolist()),
            document_id = document
        )
        
        tfidf_values.save()
        
        for term in tokens:
            print("Treated term --------------- " + term)
            try:
                inverted_index = Index.objects.get(term=term)
                if inverted_index is not None:
                    doc_ids = json.loads(inverted_index.document_ids)
                    if document.pk not in doc_ids:
                        doc_ids.append(document.pk)
                        inverted_index.document_ids = json.dumps(doc_ids)
                        inverted_index.save()
            except:
                inverted_index = Index(
                    term = term,
                    document_ids = json.dumps([document.pk])
                )
                inverted_index.save()
        
        update_tfidf_vectors()
            
        transaction.commit() # Enregistrer les modifications
        transaction.set_autocommit(True)
    except:
        transaction.rollback() # Annuler les modifications
        messages.success(request=request, message="Une erreur s'est produite")
        transaction.set_autocommit(True)
    
    end = datetime.datetime.now()
    response_time = (end - start).total_seconds()
    
    messages.success(request=request, message="Indexé en <b>" + str(response_time) + " s</b>")
    
    return redirect("client:document-list", permanent=True)

@permission_required(perm="manage-documents", login_url="/login", raise_exception=True)
def reindex(request: HttpRequest, id: int):
    start = datetime.datetime.now()
    end = None
    
    document = get_object_or_404(klass=Documents, pk=id)
    file_path = document.file_path.replace("client", "")
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = base_dir + file_path
    
    content = extract_text(file_path)
    abstract = extract_abstract(file=file_path)
    
    tokens = tokenize(content)
    vectors = vectorize(tokens=tokens)
    
    document.abstract = abstract
    document.content = content
    
    transaction.set_autocommit(False) # Commencer la transaction
    
    try:
        document.save()
        document_vector = vectors.toarray()[0]
        tfidf_values = TfidfValues.objects.get(document_id=document.pk)
        tfidf_values.tfidf_vectors = json.dumps(document_vector.tolist())
        tfidf_values.save()
        
        for term in tokens:
            print("Term treated: " + term)
            try:
                inverted_index = Index.objects.get(term=term)
                if inverted_index is not None:
                    doc_ids = json.loads(inverted_index.document_ids)
                    if document.pk not in doc_ids:
                        doc_ids.append(document.pk)
                        inverted_index.document_ids = json.dumps(doc_ids)
                        inverted_index.save()
            except:
                inverted_index = Index(
                    term = term,
                    document_ids = json.dumps([document.pk])
                )
                inverted_index.save()
        
        update_tfidf_vectors()
        
        transaction.commit() # Enregistrer les modifications
        transaction.set_autocommit(True)
    except:
        transaction.rollback() # Annuler les modifications
        transaction.set_autocommit(True)
    
    end = datetime.datetime.now()
    response_time = (end - start).total_seconds()
    
    messages.success(request=request, message="Reindexé en <b>" + str(response_time) + " s</b>")
    
    return redirect("client:document-list", permanent=True)

@permission_required(perm="manage-documents", login_url="/login", raise_exception=True)
def delete(request: HttpRequest):
    if (request.method == "GET"): raise Exception("Get method not supported for this route")
    
    id = request.POST['id']
    document = get_object_or_404(klass=Documents, pk=id)
    document.delete()
    return redirect("client:document-list")