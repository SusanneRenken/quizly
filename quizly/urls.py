"""quizly URL Configuration"""

from django.contrib import admin
from django.urls import include, path
from quizly.core.view import HealthView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/health/", HealthView.as_view(), name="health"),
    path('api/', include('auth_app.api.urls')),
    path('api/', include('management_app.api.urls')),
]
