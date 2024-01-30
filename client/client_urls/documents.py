from django.urls import path
from ..controllers import main, document, document_type

patterns = [
    path(route="document/download", view=main.download, name="download"),
    path(route="document/list", view=document.list, name="document-list"),
    path(route="document/reindex/<int:id>", view=document.reindex, name="document-reindex"),
    path(route="document/edit/<int:id>", view=document.edit, name="document-edit"),
    path(route="document/preview/<int:id>", view=document.preview, name="document-preview"),
    path(route="document/index/<int:id>", view=document.index, name="document-index"),
    path(route="document/delete", view=document.delete, name="document-delete"),
    
    path(route="document/type/new", view=document_type.create, name="document-type-create"),
    path(route="document/type/list", view=document_type.list, name="document-type-list"),
    path(route="document/type/edit/<int:id>", view=document_type.edit, name="document-type-edit"),
    path(route="document/type/delete", view=document_type.delete, name="document-type-delete"),
]