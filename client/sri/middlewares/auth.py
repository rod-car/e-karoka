from django.shortcuts import redirect
from django.http import HttpRequest

class RedirectIfAuthenticatedMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        paths = ["/login", "/register"]
        if request.user.is_authenticated and request.path in paths:
            return redirect(to="client:index")
        
        return self.get_response(request)