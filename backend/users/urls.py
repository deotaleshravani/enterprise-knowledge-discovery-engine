from django.urls import path

from .views import login_view, me_view, role_required_view

urlpatterns = [
    path("auth/login/", login_view, name="login"),
    path("auth/me/", me_view, name="me"),
    path("auth/demo/", role_required_view, name="demo-role"),
]
