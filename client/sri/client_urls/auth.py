from django.urls import path
from ..controllers import auth

patterns = [
    path(route="register", view=auth.register, name="register"),
    path(route="login", view=auth.loginUser, name="login"),
    path(route="dashboard", view=auth.dashboard, name="dashboard"),
    path(route="logout", view=auth.logoutUser, name="logout")
]