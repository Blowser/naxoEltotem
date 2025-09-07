from django.urls import path
from . import views



urlpatterns = [
    path('', views.index, name='index'),
    path('registro/', views.registrarse_view, name='registro'),

]
