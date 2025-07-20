from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('chats.urls')),  # Routes for your app
    path('api-auth/', include('rest_framework.urls')),  # ✅ This line is required
]
