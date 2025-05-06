"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from base.autodoc import schema_view
from front import views
from comments.api.auth import LoginView, RegisterView, UpdatePasswordView
from comments.api.auth.view import LogoutUserAPIView

API_URL = "api/v1/"




autodoc_urls = [
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]


auth_urls = [
    path("login/", LoginView.as_view(), name="login"),
    path("registration/", RegisterView.as_view(), name="registration"),
    path("password_update/", UpdatePasswordView.as_view(), name="password_update"),
    path("logout/", LogoutUserAPIView.as_view(), name="logout"),
    # todo реализовать refresh
]


api_urls = [
    path("comments/", include("comments.api.router")),
    path("docs/", include(autodoc_urls)),
    path("auth/", include(auth_urls)),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path(API_URL, include(api_urls)),
    path('', views.comments, name='comments'),
]


