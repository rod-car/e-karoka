from django.db import models
import textwrap
from django.shortcuts import get_object_or_404
from django.shortcuts import get_list_or_404

class Categories(models.Model):
    label = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True)
    
    def __str__(self):
        return self.label

class DocumentType(models.Model):
    label = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True)
    
    def __str__(self):
        return self.label

class University(models.Model):
    label = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True)
    is_public = models.BooleanField(default=True)
    
    def __str__(self):
        return self.label

class Documents(models.Model):
    score: float = 0.0
    terms: list = []
    
    title = models.CharField(max_length=255, unique=True)
    author = models.CharField(max_length=255, unique=False)
    content = models.TextField(unique=False)
    tokens = models.TextField(unique=False)
    abstract = models.TextField(unique=False, null=True)
    presentation_date = models.DateField(null=True)
    presentation_place = models.TextField(max_length=255, null=True)
    file_path = models.TextField(max_length=255)
    file_size = models.DecimalField(max_digits=50, decimal_places=2)
    number_cited = models.IntegerField(null=True)
    number_downloaded = models.IntegerField(null=True)
    indexed = models.BooleanField(default=False)
    
    university = models.ForeignKey(University, on_delete=models.CASCADE, null=True)
    document_type = models.ForeignKey(DocumentType, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, null=True)
    
    def set_score(self, score: float):
        self.score = score

    def get_score(self) -> float:
        return self.score
    
    def findByIds(ids: list) -> list|None:
        documents = []
        for document_id in ids:
            document = Documents.objects.get(id=document_id)
            documents.append(document)
        return documents
    
    def findByIdsWithScore(ids: dict, category: int = None, year: int = None, univ: int = None) -> list|None:
        documents = []
        for document_id, score in ids.items():
            document = Documents(**Documents.objects.filter(id=document_id).values(
                'id', 'title', 'author', 'document_type_id', 'category_id',
                'presentation_date', 'university_id', 'content', 'file_path'
            ).get())
            
            if category != None:
                c = get_object_or_404(Categories, pk=category)
                
                if (c.pk == document.category.pk):
                    document.set_score(score=score)
                    documents.append(document)
            
            if year != None:
                if document.presentation_date.year >= year :
                    document.set_score(score=score)
                    documents.append(document)
                else:
                    if document in documents: documents.remove(document)
            
            if univ != None:
                if document.university.pk == int(univ):
                    document.set_score(score=score)
                    documents.append(document)
                else:
                    if document in documents: documents.remove(document)

            if category == None and year == None and univ == None:
                document.set_score(score=score)
                documents.append(document)

        return documents

    def find(self, id: int):
        document = Documents.objects.get(id=id)
        if (document): return document
        return None

    def get_content(self, width: int = 300) -> str:
        return textwrap.shorten(text=self.content, width=width)
    
    def set_terms(self, terms: list):
        self.terms = terms
    
    def get_terms(self) -> list:
        return self.terms
    
    def get_h_content(self, width: int = 2) -> str:
        """Recuperer le contenu highlité

        Args:
            width (int, optional): _description_. Defaults to 3.

        Returns:
            str: _description_
        """
        sentences = self.content.split('.')
        terms = self.get_terms()

        highlighted_sentences = []

        for sentence in sentences:
            for term in terms:
                if term in sentence:
                    if len(highlighted_sentences) > width: break
                    if (sentence.strip() not in highlighted_sentences):
                        highlighted_sentences.append("<p>" + sentence.strip() + ".</p>")

        html_output = " ".join(highlighted_sentences)
        for term in terms:
            html_output = html_output.replace(term, "<span class='highlighted'>" + str(term) + "</span>")

        return html_output
    
    def get_h_content_full(self) -> str:
        sentences = self.content.split('.')
        terms = self.get_terms()

        highlighted_sentences = []

        for sentence in sentences:
            for term in terms:
                if term in sentence:
                    if (sentence.strip() not in highlighted_sentences):
                        highlighted_sentences.append("<p>" + sentence.strip() + "</p></br>")

        html_output = " ".join(highlighted_sentences)
        for term in terms:
            html_output = html_output.replace(term, "<span class='highlighted'>" + str(term) + "</span>")

        return html_output

    def file_type (self) -> str:
        file_type = self.file_path
        file_type = file_type.split("/")[-1].split('.')[-1].upper()
        
        return file_type

class Index(models.Model):
    """
        Modele contenant l'index inversé
    """
    term = models.TextField(max_length=255, unique=True)
    document_ids = models.TextField()

class TfidfValues(models.Model):
    document_id = models.OneToOneField(to=Documents, on_delete=models.CASCADE)
    tfidf_vectors = models.TextField()