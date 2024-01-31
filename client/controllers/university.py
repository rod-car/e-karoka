from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest
from django.contrib.auth.decorators import permission_required

from ..models import University
from ..forms import UniversityForm

from django.db import transaction
from django.contrib import messages

@permission_required(perm="manage_universities", login_url="/login", raise_exception=True)
def create(request: HttpRequest):
    if (request.method == "POST"):
        form = UniversityForm(request.POST)
        if (form.is_valid()):
            label = form.cleaned_data['label']
            description = form.cleaned_data['description']
            is_public = form.cleaned_data['is_public']
            
            university = University(
                label = label,
                description = description,
                is_public = is_public
            )

            transaction.set_autocommit(False)
            university.save()
            transaction.commit()
            transaction.set_autocommit(True)
            messages.success(request=request, message="Succès")
            
            return redirect(to="client:university-create", permanent=True)
    
    form = UniversityForm()
    return render(request=request, template_name="client/universities/new.html", context={
        "form": form
    })

@permission_required(perm="manage_universities", login_url="/login", raise_exception=True)
def list(request: HttpRequest):
    universities = University.objects.all()
    
    return render(request=request, template_name="client/universities/list.html", context={
        "universities": universities
    })

@permission_required(perm="manage_universities", login_url="/login", raise_exception=True)
def edit(request: HttpRequest, id: int):
    university = get_object_or_404(klass=University, pk=id)
    form = UniversityForm(instance=university)
    
    if (request.method == "POST"):
        form = UniversityForm(request.POST, instance=university)
        if (form.is_valid()):
            form.save(commit=True)

            return redirect(to="client:university-list", permanent=True)
    
    return render(request=request, template_name="client/universities/edit.html", context={
        "university": university,
        "form": form
    })

@permission_required(perm="manage_universities", login_url="/login", raise_exception=True)
def delete(request: HttpRequest):
    if (request.method == "GET"): raise Exception("Get method not supported for this route")
    
    id = request.POST['id']
    University = get_object_or_404(klass=University, pk=id)
    University.delete()
    return redirect("client:university-list")