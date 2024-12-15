from django.shortcuts import render
# Create your views here.
from django.http import HttpResponse
import re
from collections import defaultdict

nr_cereri = 0
suma_numere = 0

def index(request):
    return HttpResponse("Salut!")

def aduna_numere(request):
    global nr_cereri, suma_numere
    
    rezultat = re.search(r'\d+$', request.path)
    
    if rezultat:
        nr_cereri += 1
        suma_numere += int(rezultat.group())
        return HttpResponse(f"numar cereri : {nr_cereri} suma numere : {suma_numere}")
    else:
        return HttpResponse("Eroare")
    
    
def afiseaza_liste(request):
    liste = defaultdict(list)
    
    for cheie in request.GET:
        valori = request.GET.getlist(cheie)
        liste[cheie].extend(valori)
        
    raspuns = ''
    
    for cheie, valori in liste.items():
        raspuns += f"<h3>{cheie} : </h3><ul>"
        for valoare in valori:
            raspuns += f"<li>{valoare}</li>"
        raspuns += "</ul>"
        
    return HttpResponse(raspuns)


numar_nume = 0

def numara_nume(request, nume=None):
    global numar_nume
    numar_nume += 1
    return HttpResponse(f"Numarul de nume primite corect: {numar_nume}")

def cauta_subsir(request):
    lungime = 0
    rezultat = re.search(r'[0-9]*([ab]+)[0-9]*$', request.path)
    
    if rezultat:
        subsir = rezultat.group(1)
        lungime = len(subsir)
        return HttpResponse(f"Lungime subsirului {subsir} este de {lungime}")

    else:
        lungime = 0
        return HttpResponse("Nu s-a gasit un sir corespunzator")
        
    
    
def afiseaza_operatii(request):
    d={
    "lista":[{"a":10,"b":20,"operatie":"suma"},
            {"a":40,"b":20,"operatie":"diferenta"},
            {"a":25,"b":30,"operatie":"suma"},
            {"a":40,"b":30,"operatie":"diferenta"},
            {"a":100,"b":50,"operatie":"diferenta"}]
    }
    for element in d["lista"]:
        if element["operatie"] == "suma":
            element["rezultat"] = element["a"] + element["b"]
        elif element["operatie"] == "diferenta":
            element["rezultat"] = element["a"] - element["b"]
    return render(request, 'operatii.html', {'dictionar': d})
    
    
