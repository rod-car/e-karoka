from django.urls import path
from ..controllers import university

patterns = [    
    path(route="university/new", view=university.create, name="university-create"),
    path(route="university/list", view=university.list, name="university-list"),
    path(route="university/edit/<int:id>", view=university.edit, name="university-edit"),
    path(route="university/delete", view=university.delete, name="university-delete"),
]