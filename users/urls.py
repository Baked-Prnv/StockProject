from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('', views.index, name='index'),
    # path('stocktracker/', views.stockTracker, name='stocktracker'),
]
