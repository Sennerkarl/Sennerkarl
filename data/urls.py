from django.urls import path # from urls from mainproject
from .import views # import views from this directory

urlpatterns = [
    path('', views.data, name='data-main'),
    path('data-detail/', views.data_details, name='data-details'),
]