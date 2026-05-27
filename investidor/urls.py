from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views

from ativos import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home_view, name="home"),
    path(
        "login/",
        views.CustomLoginView.as_view(template_name="ativos/login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(next_page="login"), name="logout"),
    path("signup/", views.signup, name="signup"),
    path("ativos/", include("ativos.urls")),
]
