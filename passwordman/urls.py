from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('password/', include('password.urls')),
    path('organization/', include('organization.urls')),
    path('admin/', admin.site.urls),
]
