from django.http import HttpRequest, StreamingHttpResponse
from wsgiref.util import FileWrapper
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.core.files.storage import default_storage
from django.contrib.auth.decorators import login_required
import os
import mimetypes

from ..models import Documents
from ..modules.tokenizer import tokenize
from ..modules.text.spell_checker import correct_word

def preview(request: HttpRequest, id: int):
    document = get_object_or_404(klass=Documents, pk=id)
    query = ""
    
    if 'query' in request.GET: query = request.GET['query']
    
    correct_query_terms = []
    query_terms = tokenize(query)
    
    for term in query_terms:
        correct_term = correct_word(term)
        if correct_term is None:
            correct_query_terms.append(term)
        else:
            correct_query_terms.append(correct_term)
    
    query_terms = correct_query_terms
    
    document.set_terms(terms=query_terms)
    
    return render(request=request, template_name="client/preview.html", context={
        "document": document,
    })

def about(request: HttpRequest):
    return render(request=request, template_name="client/about.html", context={})

@login_required(redirect_field_name="login", login_url="/login")
def download(request: HttpRequest):
    if (request.method == "GET"): raise Exception("Get method not supported for this route")
    
    id = request.POST['document_id']
    document = get_object_or_404(klass=Documents, pk=id)
    document.number_downloaded = int(0 if document.number_downloaded == None else document.number_downloaded) + 1
    
    file_path = document.file_path.replace("client", "")
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = base_dir + file_path
    file_name = os.path.basename(file_path)
    chunk_size = 8192
    
    response = StreamingHttpResponse(
        FileWrapper(open(file_path, "rb"), chunk_size),
        content_type=mimetypes.guess_type(file_path)[0]
    )
    response['Content-Length'] = os.path.getsize(file_path)
    response['Content-Disposition'] = "Attachment;filename=%s" % file_name

    document.save()
    return response