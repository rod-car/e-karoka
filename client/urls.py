from django.urls import path
from .client_urls import auth, documents, universities
from .controllers import main, search, upload, category

app_name = "client"

urlpatterns = [
    path(route="", view=search.index, name="index"),
    path(route="about", view=main.about, name="about"),
    path(route="document/<int:id>", view=main.preview, name="preview"),
    path(route="upload", view=upload.upload, name="upload"),
    path(route="categorie/nouveau", view=category.create, name="category-create"),
    path(route="categorie/liste", view=category.list, name="category-list"),
    path(route="categorie/editer/<int:id>", view=category.edit, name="category-edit"),
    path(route="categorie/supprimer", view=category.delete, name="category-delete"),
]
urlpatterns.extend(documents.patterns)
urlpatterns.extend(auth.patterns)
urlpatterns.extend(universities.patterns)