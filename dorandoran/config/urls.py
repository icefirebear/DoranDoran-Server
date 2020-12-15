"""dorandoran URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include
from .yasg import *

schema_url_patterns =[
    
    path("auth/", include("account.urls")),
    path("team/", include("team.urls")),
    path("room/", include("room.urls")),
]

schema_view = get_schema_view(
    openapi.Info(
        title="DoranDoran Open API",
        default_version="v1",
        terms_of_service="https://www.google.com/policies/terms/",
    ),
    public=True,
    patterns=schema_url_patterns,
)

urlpatterns = [
    
    path("auth/", include("account.urls")),
    path("team/", include("team.urls")),
    path("room/", include("room.urls")),
    path(
        "swagger<str:format>",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("docs/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
