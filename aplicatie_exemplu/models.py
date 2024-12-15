from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser

class Organizator(models.Model):
    nume = models.CharField(max_length=100)
    email = models.EmailField()

class Locatie(models.Model):
    adresa = models.CharField(max_length=255)
    oras = models.CharField(max_length=100)
    judet = models.CharField(max_length=100)
    cod_postal = models.CharField(max_length=10)
    
class Eveniment(models.Model):
    id_eveniment = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    titlu = models.CharField(max_length=200)
    descriere = models.TextField()
    TIPURI_EVENIMENT = [
        ('conferinta', 'Conferinta'), ('workshop', 'Workshop'),
        ('intalnire', 'Intalnire'), ('webinar', 'Webinar')]
    tip_eveniment = models.CharField(max_length=50, choices=TIPURI_EVENIMENT)
    organizator = models.ForeignKey(Organizator, on_delete=models.CASCADE, related_name="evenimente")
    locatie = models.ForeignKey(Locatie, on_delete=models.SET_NULL, null=True)
    capacitate = models.PositiveIntegerField()
    este_public = models.BooleanField(default=True)
    imagine = models.ImageField(upload_to='imagini_evenimente/', null=True, blank=True)
    website = models.URLField(blank=True)
    slug = models.SlugField(unique=True)
    data_creare = models.DateTimeField(auto_now_add=True)
    data_actualizare = models.DateTimeField(auto_now=True)
    
class Prajitura(models.Model):
    nume = models.CharField(max_length=20, unique=True)
    descriere = models.TextField(null = True)
    pret = models.DecimalField(max_digits=8, decimal_places=2)
    gramaj = models.PositiveBigIntegerField()
    temperatura = models.IntegerField()
    TIPURI_PRODUSE = [
        ('cofetarie', 'Cofetarie'),
        ('patiserie', 'Patiserie'),
        ('gelaterie', 'Gelaterie')
    ]
    tip_produs = models.CharField(max_length=50, choices=TIPURI_PRODUSE, default='cofetarie', null=True)
    calorii = models.IntegerField()
    CATEG_PRAJITURA = [
        ('comanda speciala', 'Comanda speciala'),
        ('aniversara', 'Aniversara'),
        ('editie limitata', 'Editie limitata'),
        ('pentru copii', 'Pentru copii'),
        ('dietetica', 'Dietetica'),
        ('comuna', 'Comuna')
    ]
    categorie = models.CharField(max_length=50, choices=CATEG_PRAJITURA, default='comuna', null=True)
    pt_diabetici = models.BooleanField(default=False)
    imagine = models.ImageField(upload_to='imagini_prajituri/', null=True, blank=True)
    data_adaugare = models.DateTimeField(auto_now_add=True, null=True)
    
    ingrediente = models.ManyToManyField('Ingredient') #many-to-many cu ingredient
    ambalaj = models.ForeignKey('Ambalaj', on_delete=models.CASCADE, null=True, blank=True) #one-to-many cu ambalaj
    #ambalaj = models.ForeignKey('Ambalaj', on_delete=models.CASCADE, default = 1) #dupa ce populez Ambalaj

    
class IngredientPrajitura(models.Model):
    nume = models.CharField(max_length=30, unique=True)
    calorii = models.IntegerField()
    unitate = models.CharField(max_length=10)
    
class AmbalajPrajitura(models.Model):
    nume = models.CharField(max_length=20, unique=True)
    MATERIALE = [
        ('plastic', 'Plastic'),
        ('hartie', 'Hartie'),
        ('carton', 'Carton')
    ]
    material = models.CharField(max_length=10, choices=MATERIALE)
    pret = models.DecimalField(max_digits=5, decimal_places=2)
    
    
class Meniu(models.Model):
    nume = models.CharField(max_length=50, unique=True)
    descriere = models.TextField(null=True, blank=True)
    data_creare = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return self.nume
    
class Pizza(models.Model):
    nume = models.CharField(max_length=100, unique=True)
    descriere = models.TextField(null=True, blank=True)
    pret = models.DecimalField(max_digits=6, decimal_places=2)
    gramaj = models.PositiveIntegerField()
    
    meniu = models.ForeignKey('Meniu', on_delete=models.CASCADE) #one-to-many cu meniu
    ingrediente = models.ManyToManyField('Ingredient') #many-to-many cu ingredient
    ambalaj = models.ForeignKey('Ambalaj', on_delete=models.CASCADE, null=True, blank=True) #one-to-many cu ambalaj
    
    
    def __str__(self):
        return self.nume

    
class Ingredient(models.Model):
    nume = models.CharField(max_length=100, unique=True)
    calorii = models.PositiveIntegerField()
        
    def __str__(self):
        return self.nume
    
class Comanda(models.Model):
    id_comanda = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    nume_client = models.CharField(max_length=100)
    data_comanda = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    
    pizzas = models.ManyToManyField('Pizza') #many-to-many cu pizza
    
    def calculeaza_total(self):
        total = sum(pizza.pret_total() for pizza in self.pizzas.all())
        self.total = total
        self.save()
        return total
    
    def __str__(self):
        return f"Comanda {self.id_comanda} - {self.nume_client}"

    
class Ambalaj(models.Model):
    nume = models.CharField(max_length=20, unique=True)
    MATERIALE = [
        ('plastic', 'Plastic'),
        ('carton', 'Carton'),
    ]
    material = models.CharField(max_length=20, choices=MATERIALE, default='carton')
    
    def __str__(self):
        return self.nume
    
class CustomUser(AbstractUser):
    telefon = models.CharField(max_length=15, blank=True)
    data_nasterii = models.DateField(null=True, blank = True)
    adresa = models.CharField(max_length=255, blank=True)
    oras = models.CharField(max_length=100, blank=True)
    newsletter = models.BooleanField(default=False)

    def __str__(self):
        return self.username


    