from django.urls import path
from app.dashboard.views.base import Index

urlpatterns = [
    path('', Index.as_view())
]