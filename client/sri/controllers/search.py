import json, datetime
import numpy as np

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from django.core.paginator import Paginator

from ..modules.tokenizer import tokenize, remove_accents_french
from ..modules.text_processing import preprocess_text
from ..modules.text.spell_checker import correct_word
from ..modules.constants import SIMILARITY_THRESHOLD, YEARS

from ..models import Documents, Index, TfidfValues, Categories, University

def index(request: HttpRequest) -> HttpResponse:
    """Page de recherche et traite l'appariément requête-documents

    Args:
        request (HttpRequest): Requête contenant les mots clés de l'utilisateur

    Returns:
        HttpResponse: Page de recherche ou Page de resultats de recherche
    """
    
    query = request.GET.get('query', default='').strip()
    filter_field = request.GET.get('filter', default='content').strip()
    category_id = int(request.GET.get('category', default=0))
    year = int(request.GET.get('year', default=0))
    univ = int(request.GET.get('univ', default=-1))

    if (query != ""):
        start = datetime.datetime.now()
        end = None
        
        documents = []
        query_terms = []
        
        inverted_indexes = Index.objects.all()
        
        if (inverted_indexes.count() > 0):
            terms = [preprocess_text(inverted_index.term) for inverted_index in inverted_indexes]

            vectorizer = TfidfVectorizer(lowercase=True, sublinear_tf=True)
            vectorizer.fit_transform(terms)

            correct_query_terms = []
            query_terms = tokenize(query)
            
            for term in query_terms:
                correct_term = correct_word(term)
                if correct_term is None:
                    correct_query_terms.append(term)
                else:
                    correct_query_terms.append(correct_term)
            
            query_terms = correct_query_terms
            text = remove_accents_french(" ".join(query_terms))
            query_vector = vectorizer.transform([text]).toarray()[0]
            
            if (filter_field == "content"):
                selected_docs = search(query_vector=query_vector)
                if (len(selected_docs) > 0):
                    documents = Documents.findByIdsWithScore(
                        ids = selected_docs,
                        category = None if category_id <= 0 else category_id,
                        year = None if year <= 0 else year,
                        univ = None if univ <= 0 else univ
                    )
            else:
                if filter_field == "author": 
                    query_terms = query.split()
                    documents = searchBy(query_terms=query_terms, query_vector=query_vector, field=filter_field)
                else:
                    selected_docs = searchBy(query_terms=query_terms, query_vector=query_vector, field=filter_field)
                    if (len(selected_docs) > 0):
                        documents = Documents.findByIdsWithScore(
                            ids = selected_docs, 
                            category = None if category_id < 0 else category_id,
                            year = None if year <= 0 else year,
                            univ = None if univ <= 0 else univ
                        )
        else:
            pass

        for d in documents:
            d.set_terms(query_terms)
        
        page_number = int(request.GET.get('page', default=1))
        per_page = int(request.GET.get('perpage', default=10))
        
        paginator = Paginator(object_list=documents, per_page=per_page)
        page_obj = paginator.get_page(number=page_number)
        
        end = datetime.datetime.now()
        response_time = (end - start).total_seconds()
        
        return render(request=request, template_name="client/results.html", context={
            "query": query,
            "page_obj": page_obj,
            "filter_field": filter_field,
            "per_page": per_page,
            "response_time": response_time,
            "categories": Categories.objects.all(),
            "category_id": category_id,
            "years": YEARS,
            "current_year": year,
            "universities": University.objects.all(),
            "current_univ": univ
        })
    else:
        if (request.session.has_key('query')):
            request.session.pop('query')
        
    return render(request=request, template_name="client/search.html", context={
        "query": query
    })

def cosine_similarity_score(vector1, vector2):
    return cosine_similarity([vector1], [vector2])[0][0]

def searchBy(query_terms, query_vector, field = "title"):
    document_scores = []

    for term in query_terms:
        filter_kwargs = {f"{field}__icontains": term}
        documents = Documents.objects.filter(**filter_kwargs)

        if (field != "author"):
            for document in documents:
                try:
                    tfidf_value = TfidfValues.objects.get(document_id=document.pk)
                    tfidf_vector_json = json.loads(tfidf_value.tfidf_vectors)
                    
                    tfidf_vector = np.array(tfidf_vector_json)
                    similarity_score = cosine_similarity_score(query_vector, tfidf_vector)
                    document_scores.append((document.pk, similarity_score))
                except:
                    pass
    if (field == "author"): return documents
    
    combined_scores = {}
    for doc_id, similarity_score in document_scores:
        if doc_id in combined_scores:
            combined_scores[doc_id] += similarity_score
        else:
            combined_scores[doc_id] = similarity_score

    sorted_results = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)

    similar_documents = {}
    for doc_id, similarity_score in sorted_results:
        if (similarity_score >= SIMILARITY_THRESHOLD):
            similar_documents[doc_id] = similarity_score

    return similar_documents

def search(query_vector: list) -> dict:
    tfidf_records = TfidfValues.objects.all()
    doc_ids = [record.document_id_id for record in tfidf_records]
    
    tfidf_vectors = [json.loads(record.tfidf_vectors) for record in tfidf_records]
    
    similarities = [np.dot(query_vector, doc_vector) / (np.linalg.norm(query_vector) * np.linalg.norm(doc_vector)) for doc_vector in tfidf_vectors]

    doc_similarity_pairs = list(zip(doc_ids, similarities))
    sorted_doc_similarity_pairs = sorted(doc_similarity_pairs, key=lambda x: x[1], reverse=True)

    similar_documents = {doc_id: similarity for doc_id, similarity in sorted_doc_similarity_pairs if similarity > SIMILARITY_THRESHOLD}
    
    return similar_documents