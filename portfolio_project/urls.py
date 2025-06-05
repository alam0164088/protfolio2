from django.contrib import admin
from django.urls import path, include  # Include core.urls, not portfolio_project.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),  # Include the URLs from core app
]
