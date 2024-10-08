from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrdersViewSet


urlpatterns = [
    path('order/', OrdersViewSet.as_view({'post': 'create'})),
]