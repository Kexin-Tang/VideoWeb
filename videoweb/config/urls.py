from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('client/', include('app.client.urls')),
    path('dashboard/', include('app.dashboard.urls'))
]
