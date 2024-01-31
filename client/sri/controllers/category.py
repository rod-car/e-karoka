from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required, permission_required

from ..models import Categories
from ..forms import CategoryForm

from django.db import transaction

@permission_required(perm="manage-category", login_url="/login", raise_exception=True)
def create(request: HttpRequest):
    if (request.method == "POST"):
        form = CategoryForm(request.POST)
        if (form.is_valid()):
            label = form.cleaned_data['label']
            description = form.cleaned_data['description']
            
            category = Categories(
                label = label,
                description = description
            )
            transaction.set_autocommit(False)
            category.save()
            transaction.commit()
            transaction.set_autocommit(True)
            
            return redirect(to="client:category-create", permanent=True)
    
    form = CategoryForm()
    return render(request=request, template_name="client/categories/new.html", context={
        "form": form
    })

@permission_required(perm="manage-category", login_url="/login", raise_exception=True)
def list(request: HttpRequest):
    categories = Categories.objects.all()
    
    return render(request=request, template_name="client/categories/list.html", context={
        "categories": categories
    })

@permission_required(perm="manage-category", login_url="/login", raise_exception=True)
def edit(request: HttpRequest, id: int):
    category = get_object_or_404(klass=Categories, pk=id)
    
    if (request.method == "POST"):
        form = CategoryForm(request.POST)
        if (form.is_valid()):
            label = form.cleaned_data['label']
            description = form.cleaned_data['description']
            
            category.label = label
            category.description = description
            
            category.save()
            return redirect(to="client:category-list", permanent=True)
    
    return render(request=request, template_name="client/categories/edit.html", context={
        "category": category
    })

@permission_required(perm="manage-category", login_url="/login", raise_exception=True)
def delete(request: HttpRequest):
    if (request.method == "GET"): raise Exception("Get method not supported for this route")
    
    id = request.POST['id']
    category = get_object_or_404(klass=Categories, pk=id)
    category.delete()
    return redirect("client:category-list")