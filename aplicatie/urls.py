from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    re_path(r'^pag/[a-zA-Z0-9]*\d+$', views.aduna_numere, name="aduna_numere"),
    path("liste", views.afiseaza_liste, name="afiseaza_liste"),
    re_path(r'^nume_corect/[A-Z][a-z]*(-[A-Z][a-z]*)?\+[A-Z][a-z]*$', views.numara_nume, name="numara_nume"),
    re_path(r'^subsir/[0-9]*[ab]+[0-9]*$', views.cauta_subsir, name="cauta_subsir"),
    path('operatii/', views.afiseaza_operatii, name="afiseaza_operatii"),
]