from django.urls import path # from urls from mainproject
from .import views # import views from this directory

urlpatterns = [
    path('', views.DataView.as_view(), name='data-main'),
]