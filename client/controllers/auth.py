from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from ..forms import RegisterForm

def register(request: HttpRequest) -> HttpResponse:
    form = RegisterForm()
    
    if (request.method == "POST"):
        form = RegisterForm(request.POST)
        if (form.is_valid()):
            form.save()
            messages.success(request=request, message="Compte crée avec succès")
            
            return redirect(to="client:register", permanent=True)
        
    return render(request=request, template_name="client/auth/register.html", context={
        "form": form
    })

def loginUser(request: HttpRequest) -> HttpResponse:
    form = AuthenticationForm()
    
    if (request.method == "POST"):
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request=request, username=username, password=password)

        if user is not None:
            login(request, user)
            
            redirect_url = request.GET['login'] if "login" in request.GET else None
            if (redirect_url != None): return redirect(to=redirect_url)
            return redirect(to="client:index")
        else:
            messages.error(request=request, message="Impossible de trouver le compte")
    
    return render(request=request, template_name="client/auth/login.html", context={
        "form": form
    })

@login_required(redirect_field_name="login", login_url="/login")
def dashboard(request: HttpRequest) -> HttpResponse:
    """Acceder au dashboard de l'utilisateur

    Args:
        request (HttpRequest): Requête contenant l'utilisateur connecté

    Returns:
        HttpResponse: Page du dashboard
    """
    return render(request=request, template_name="client/auth/dashboard.html", context={})

@login_required(redirect_field_name="login", login_url="/login")
def logoutUser(request: HttpRequest) -> HttpResponse:
    """Permet de deconnecter un utilisateur

    Args:
        request (HttpRequest): Requête contenant l'information de l'utilisateur

    Returns:
        HttpResponse: Redirection vers la page de connexion
    """
    logout(request=request)
    return redirect(to="client:index", permanent=True)