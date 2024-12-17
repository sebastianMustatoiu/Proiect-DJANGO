import re
import os
import json
from django.contrib.auth import logout
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from datetime import datetime
from django.utils import timezone
from django.core.paginator import Paginator
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .models import CustomUser, Vizualizari, Pizza, Promotie
from django.core.mail import send_mass_mail
from django.db.models import Count
from django.db import models

from .models import Locatie, Prajitura, Pizza, CustomUser
from .forms import PizzaFilterForm, ContactForm, PizzaForm, CustomUserCreationForm, CustomAuthenticationForm, PromotieForm


accesari = 0
valori_t = []

def index(request):
    trimite_email()
    return HttpResponse("Primul raspuns")



def pag1(request):
    return HttpResponse(2+3)



l=[]
def pag2(request):
    global l
    a=request.GET.get("a",10)
    print(request.GET)
    l.append(a)
    return HttpResponse(f"<b>Am primit</b>: {l}")

#Ex1, lab1
def mesaj(request):
    return HttpResponse("Buna ziua!")

#Ex2, lab1
def data(request):
    current_time = datetime.now()
    return HttpResponse(f"Data si ora curenta : {current_time}")

#Ex3, lab1
def nr_accesari(request):
    global accesari
    accesari+=1
    return HttpResponse(f"Numarul de accesari de cand a fost pornit serverul este: {accesari}")

#Ex4, lab1
def suma(request):
    suma = 0
    a=int(request.GET.get("a", 0))
    b=int(request.GET.get("b", 0))
    suma = a+b
    return HttpResponse(f"Suma celor 2 variabile este: {a+b}")

#Ex4, lab1, varianta2
def suma2(request, a, b):
    return HttpResponse(f"Suma celor 2 variabile {a} si {b} este : {a+b}")

#Ex5, lab1
def text(request):
    global valori_t
    valoare=request.GET.get("t", "")
    if valoare.isalpha():
        valori_t.append(valoare)
    raspuns = "".join(f"<p>{v}</p>" for v in valori_t)
    return HttpResponse(raspuns)

#Ex6, lab1
def nr_parametri(request):
    numar = len(request.GET)
    return HttpResponse(f"Numarul de parametri primiti este de: {numar}")
    
#Ex7, lab1
def operatie(request):
    a = int(request.GET.get("a", 0))
    b = int(request.GET.get("b", 0))
    op = request.GET.get("op", "")
    if op == "sum":
        return HttpResponse(f"Suma celor 2 numere {a} si {b} este de : {a+b}")
    elif op == "dif":
        return HttpResponse(f"Diferenta celor 2 numere {a} si {b} este de : {a-b}")
    elif op == "mul":
        return HttpResponse(f"Inmultirea celor 2 numere {a} si {b} este de : {a*b}")
    elif op == "div":
        return HttpResponse(f"Impartirea celor 2 numere {a} si {b} este de : {a/b}")
    elif op == "mod":
        return HttpResponse(f"Modulul celor 2 numere {a} si {b} este de : {a%b}")


#Ex8, lab1
def tabel(request):
    matrice = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]
    tabel = "<table border = '1'>"
    for i in matrice:
        tabel += "<tr>"
        for j in i:
            tabel += f"<td>{j}</td>"
        tabel += "</tr>"
    tabel += "</table>"
    
    return HttpResponse(tabel)


#Ex9, lab1
def lista(request):
    lista_initiala = ["unu", "doi", "trei", "patru", "cinci", "sase", "sapte", "opt", "noua", "zece"]
    cuvinte = request.GET.get("cuvinte", "").split(",")
    
    lista_afisata = "<ul>"
    
    for cuvant in lista_initiala:
        if cuvant in cuvinte:
            lista_afisata += f"<li style='color : red;'>{cuvant}</li>"
        else:
            lista_afisata += f"<li>{cuvant}</li>"
            
    lista_afisata += "</ul>"
    return HttpResponse(lista_afisata)

def afis_template(request):
    return render(request,"articole.html",
        {
            "locatii":Locatie.objects.all()
        }
    )

def lista_prajituri(request):
    prajituri = Prajitura.objects.all()
    return render(request, 'prajituri.html', {'prajituri':Prajitura.objects.all()})


def lista_pizze(request):
    pizze = Pizza.objects.all()
    form = PizzaFilterForm(request.GET)

    if form.is_valid():
        if form.cleaned_data.get('nume'):
            pizze = pizze.filter(nume__icontains=form.cleaned_data['nume'])
        if form.cleaned_data.get('pret_min') is not None:
            pizze = pizze.filter(pret__gte=form.cleaned_data['pret_min'])
        if form.cleaned_data.get('pret_max') is not None:
            pizze = pizze.filter(pret__lte=form.cleaned_data['pret_max'])
        if form.cleaned_data.get('gramaj_min') is not None:
            pizze = pizze.filter(gramaj__gte=form.cleaned_data['gramaj_min'])
        if form.cleaned_data.get('gramaj_max') is not None:
            pizze = pizze.filter(gramaj__lte=form.cleaned_data['gramaj_max'])
        if form.cleaned_data.get('meniu'):
            pizze = pizze.filter(meniu=form.cleaned_data['meniu'])

    paginator = Paginator(pizze, 5)
    page_number = request.GET.get('page')
    paginated_pizze = paginator.get_page(page_number)

    context = {
        'form': form,
        'pizze': paginated_pizze,
    }
    return render(request, 'pizzas.html', context)

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            nume = form.cleaned_data['nume']
            prenume = form.cleaned_data['prenume']
            data_nasterii = form.cleaned_data['data_nasterii']
            email = form.cleaned_data['email']
            tip_mesaj = form.cleaned_data['tip_mesaj']
            subiect = form.cleaned_data['subiect']
            zile_asteptare = form.cleaned_data['zile_asteptare']
            mesaj = form.cleaned_data['mesaj']
            
            mesaj_data = {
                'nume': nume,
                'prenume': prenume,
                'data_nasterii': data_nasterii,
                'email': email,
                'tip_mesaj': tip_mesaj,
                'subiect': subiect,
                'zile_asteptare': zile_asteptare,
                'mesaj': mesaj,
                'timestamp': int(datetime.timestamp(datetime.now()))
            }
            
            folder_path = os.path.join(settings.BASE_DIR, 'mesaje')
            if not os.path.exists(folder_path): 
                os.makedirs(folder_path)

            file_path = os.path.join(folder_path, f"mesaj_{mesaj_data['timestamp']}.json")
            with open(file_path, 'w') as f:
                json.dump(mesaj_data, f, indent=4)

            return redirect('mesaj_trimis')
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})

def mesaj_trimis_view(request):
    return render(request, 'mesaj_trimis.html') 

def adauga_pizza(request):
    if request.method == 'POST':
        form = PizzaForm(request.POST)
        if form.is_valid():
            pizza = form.save(commit=False)
            
            if form.cleaned_data.get('discount') is not None:
                pizza.pret = pizza.pret - (pizza.pret * form.cleaned_data['discount'] / 100)
            
            pizza.save()

            return redirect('lista_pizze')
    else:
        form = PizzaForm()

    return render(request, 'adaugare_pizza.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'inregistrare.html', {'form': form})

def home(request):
    return HttpResponse("Acasa!")

def custom_login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST, request=request)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if not form.cleaned_data.get('ramane_logat'):
                request.session.set_expiry(0)
            else:
                request.session.set_expiry(24*60*60)    
            return redirect('profile')
    else:
        form = CustomAuthenticationForm()

    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def profile_view(request):
    request.session['username'] = request.user.username
    request.session['email'] = request.user.email
    request.session['telefon'] = request.user.telefon
    request.session['data_nasterii'] = request.user.data_nasterii.strftime('%Y-%m-%d') if request.user.data_nasterii else None
    request.session['adresa'] = request.user.adresa
    request.session['oras'] = request.user.oras
    
    context = {
        'username': request.session['username'],
        'email': request.session['email'],
        'telefon': request.session['telefon'],
        'data_nasterii': request.session['data_nasterii'],
        'adresa': request.session['adresa'],
        'oras': request.session['oras'],
    }
    return render(request, 'profile.html', context)


def trimite_email():
    send_mail(
        subject='Salutare!',
        message='Salut. Ce mai faci?',
        html_message='<h1>Salut</h1><p>Ce mai faci?</p>',
        from_email='sebim5764@gmail.com',
        recipient_list=['sebim5764@gmail.com'],
        fail_silently=False,
    )

def confirma_mail(request, cod):
    try:
        user = CustomUser.objects.get(cod=cod)
        if user.email_confirmat:
            mesaj = "Emailul a fost deja confirmat."
        else:
            user.email_confirmat = True
            user.cod = None
            user.save()
            mesaj = "Felicitari! Emailul tau a fost confirmat cu succes."

    except CustomUser.DoesNotExist:
        mesaj = "Codul de confirmare este invalid sau a expirat."

    return render(request, 'confirmare_email.html', {'mesaj': mesaj})

MAX_VIZUALIZARI = 5
K_VIZUALIZARI = 2

def adauga_vizualizare(user, produs):
    Vizualizari.objects.create(user=user, produs=produs)

    vizualizari = Vizualizari.objects.filter(user=user).order_by('-data_vizualizare')
    if vizualizari.count() > MAX_VIZUALIZARI:
        vizualizari.last().delete()
        
def adauga_promotie(request):
    if request.method == 'POST':
        form = PromotieForm(request.POST)
        if form.is_valid():
            promotie = form.save()

            meniuri_selectate = form.cleaned_data['meniu']

            utilizatori = CustomUser.objects.annotate(
                vizualizari_count=Count('vizualizari', filter=models.Q(
                    vizualizari__produs__meniu__in=meniuri_selectate
                ))
            ).filter(vizualizari_count__gte=K_VIZUALIZARI, newsletter=True).distinct()

            mailuri = []
            for user in utilizatori:
                mesaj_html = render_to_string('email_promotie.html', {
                    'nume': user.username,
                    'nume_promotie': promotie.nume,
                    'data_expirare': promotie.data_expirare,
                    'discount': promotie.discount,
                    'mesaj_personalizat': promotie.mesaj_personalizat,
                })
                mesaj = (
                    f"Promoție: {promotie.nume}",
                    mesaj_html,
                    'sebim5764@gmail.com',
                    [user.email],
                )
                mailuri.append(mesaj)

            send_mass_mail(mailuri, fail_silently=False)
            return redirect('lista_promotii')
    else:
        form = PromotieForm()
    return render(request, 'adauga_promotie.html', {'form': form})

def lista_promotii(request):
    promotii = Promotie.objects.all()
    return render(request, 'lista_promotii.html', {'promotii': promotii})

@login_required
def detalii_pizza(request, id):
    pizza = get_object_or_404(Pizza, id=id)
    adauga_vizualizare(request.user, pizza)
    return render(request, 'detalii_pizza.html', {'pizza': pizza})
