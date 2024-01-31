import numpy as np
import json, datetime
from django.db import transaction
from django.contrib import messages
from django.http import HttpRequest
from django.core.files.storage import default_storage
from django.contrib.auth.decorators import login_required
from sklearn.feature_extraction.text import TfidfVectorizer
from django.shortcuts import render, redirect, get_object_or_404

from ..modules.tokenizer import tokenize
from ..modules.vectorizer import vectorize
from ..modules.text_processing import preprocess_text
from ..modules.text_extractor import extract_text, extract_abstract
from ..models import Documents, Index, TfidfValues, Categories, DocumentType, University

@login_required(redirect_field_name="login", login_url="/login")
def upload(request: HttpRequest):
    if (request.method == 'POST'):
        start = datetime.datetime.now()
        end = None
        response_time: float = 0.0
        
        title = request.POST['title']
        author = request.POST['author']
        presentation_date = request.POST['presentation_date']

        category = get_object_or_404(klass=Categories, pk=int(request.POST['category']))
        document_type = get_object_or_404(klass=DocumentType, pk=int(request.POST['document_type']))
        university = get_object_or_404(klass=University, pk=int(request.POST['university']))
        
        doc_file = request.FILES['document']
        
        size = doc_file.size
        document_already_exist = default_storage.exists("client/documents/" + doc_file.name)
        
        if (document_already_exist):
            file_name = "client/documents/" + doc_file.name
        else:
            file_name = default_storage.save("client/documents/" + doc_file.name, doc_file)

        doc_file = default_storage.open(file_name)
        content = extract_text(doc_file.name)
        abstract = extract_abstract(file=doc_file.name)
        
        tokens =  tokenize(content) if request.user.is_superuser else []
        vectors =  vectorize(tokens=tokens) if request.user.is_superuser else []
        
        document = Documents(
            title = title,
            author = author,
            category = category,
            document_type = document_type,
            university = university,
            content = content,
            tokens = tokens,
            file_path = file_name,
            file_size = size,
            abstract = abstract,
            presentation_date = presentation_date,
            indexed = False
        )
        
        transaction.set_autocommit(False)
        
        try:
            document.save()
            if (request.user.is_superuser):
                document_vector = vectors.toarray()[0]
                tfidf_values = TfidfValues(
                    tfidf_vectors = json.dumps(document_vector.tolist()),
                    document_id = document
                )
                
                tfidf_values.save()
                
                for term in tokens:
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
        
        messages.success(request=request, message="Document deposé avec succès en " + str(response_time) + " S")

        return redirect("client:upload", permanent=True)
    
    return render(request=request, template_name="client/upload.html", context={
        "categories": Categories.objects.all(),
        "universities": University.objects.all(),
        "document_types": DocumentType.objects.all()
    })

def handle_uploaded_file(f, folder):
    with open(folder, "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def update_tfidf_vectors():
    inverted_indexes = Index.objects.all()
    terms = [inverted_index.term for inverted_index in inverted_indexes]
    terms = [preprocess_text(term) for term in terms]

    vectorizer = TfidfVectorizer()
    vectorizer.fit_transform(terms)
    
    tfidf_values = TfidfValues.objects.all()
    doc_ids = [tfidf_value.document_id_id for tfidf_value in tfidf_values]
    
    for doc_id in doc_ids:
        document_terms = Documents.objects.get(pk=doc_id).content.split()
        document_vector = vectorizer.transform([" ".join(document_terms)]).toarray()[0]

        document_vector = np.round(document_vector, 4)
        document_vector_json = json.dumps(document_vector.tolist())  # Convert to JSON
        
        tfidf_value = TfidfValues.objects.get(document_id=doc_id)
        tfidf_value.tfidf_vectors = document_vector_json
        tfidf_value.save()