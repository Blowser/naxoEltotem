from django.urls import path
from . import views



urlpatterns = [
    path('', views.index, name='index'),
    path('registrarse/', views.registrarse_view, name='registrarse'),
    path('login/', views.login_view, name='login'),
    path('noticias/', views.NoticiasFiltradasView.as_view(), name='noticias'),
    path('scrap-yugioh/', views.scrap_yugioh, name='scrap_yugioh'),

]
