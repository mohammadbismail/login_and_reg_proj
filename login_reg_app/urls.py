from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("register/", views.register_user),
    path("login/", views.check_login),
    # path("success/", views.success_page),
    path("success/<int:user_id>", views.success_page),
    path("logout/", views.logout_user),
]
