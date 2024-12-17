from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("pag1", views.pag1, name="f"),
    path("pag2", views.pag2, name="g"),
    path("mesaj", views.mesaj, name="mesaj"),
    path("data", views.data, name="data"),
    path("nr_accesari", views.nr_accesari, name="nr_accesari"),
    path("suma", views.suma, name="suma"),
    path("suma2/<int:a>/<int:b>/", views.suma2, name="suma2"),
    path("text", views.text, name="text"),
    path("nr_parametri", views.nr_parametri, name="nr_parametri"),
    path("operatie", views.operatie, name="operatie"),
    path("tabel", views.tabel, name="tabel"),
    path("lista", views.lista, name="lista"),
    path('afis_template/', views.afis_template, name="afis_template"),
    path('prajituri/', views.lista_prajituri, name='lista_prajituri'),
    path('lista_pizze/', views.lista_pizze, name="lista_pizze"),
    path('contact/', views.contact_view, name='contact'),
    path('mesaj_trimis/', views.mesaj_trimis_view, name='mesaj_trimis'),
    path('adauga_pizza/', views.adauga_pizza, name='adauga_pizza'),
    path('home', views.home, name="home"),
    path('login', views.custom_login_view, name="login"),
    path('inregistrare', views.register_view, name="register_view"),
    path('logout', views.logout_view, name="logout"),
    path('profile/', views.profile_view, name='profile'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='password_change.html'), name='password_change'),
    path('password_change_done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'), name='password_change_done'),
    path('confirma_mail/<str:cod>/', views.confirma_mail, name='confirma_mail'),

]
