from django.urls import path, include
from django.contrib import admin


urlpatterns = [
    path('admin/', admin.site.urls),
    path('social/', include('allauth.urls')),
    path('accounts/', include('accounts.urls')),
]
