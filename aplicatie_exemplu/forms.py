from django import forms
from django.core.exceptions import ValidationError
from datetime import datetime
from .models import Meniu, Pizza
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from .models import CustomUser
import re
import datetime
import uuid
from django.template.loader import render_to_string
from django.core.mail import EmailMessage



class PizzaFilterForm(forms.Form):
    nume = forms.CharField(label="Nume Pizza", required=False, max_length=100)
    pret_min = forms.DecimalField(label="Pret minim", required=False, min_value=0, decimal_places=2)
    pret_max = forms.DecimalField(label="Pret maxim", required=False, min_value=0, decimal_places=2)
    gramaj_min = forms.IntegerField(label="Gramaj minim", required=False, min_value=0)
    gramaj_max = forms.IntegerField(label="Gramaj maxim", required=False, min_value=0)
    meniu = forms.ModelChoiceField(
        queryset=Meniu.objects.all(),
        label="Meniu",
        required=False,
        empty_label="Oricare"
    )

class ContactForm(forms.Form):
    nume = forms.CharField(label="Nume", max_length=10, required=True)
    prenume = forms.CharField(label="Prenume", max_length=10, required=False)
    data_nasterii = forms.DateField(label="Data nasterii", widget=forms.DateInput(attrs={'type': 'date'}), required=True)
    email = forms.EmailField(label="E-mail", required=True)
    confirmare_email = forms.EmailField(label="Confirmare e-mail", required=True)
    tip_mesaj = forms.ChoiceField(choices=[
        ('reclamatie', 'Reclamatie'),
        ('intrebare', 'Intrebare'),
        ('review', 'Review'),
        ('cerere', 'Cerere'),
        ('programare', 'Programare')
    ], required=True)
    subiect = forms.CharField(max_length=100, required=True, label="Subiect")
    zile_asteptare = forms.IntegerField(min_value=1, required=True, label="Minim zile asteptare")
    mesaj = forms.CharField(widget=forms.Textarea, required=True, label="Mesaj")
    
    def clean_confirmare_email(self):
        email = self.cleaned_data.get('email')
        confirmare_email = self.cleaned_data.get('confirmare_email')
        if email != confirmare_email:
            raise ValidationError("Adresele de email nu coincid.")
        return confirmare_email

    def clean(self):
        cleaned_data = super().clean()
        nume = cleaned_data.get("nume")
        prenume = cleaned_data.get("prenume")
        subiect = cleaned_data.get("subiect")

        if nume and not nume[0].isupper():
            raise ValidationError("Numele trebuie sa inceapa cu litera mare.")
        if prenume and not prenume[0].isupper():
            raise ValidationError("Prenumele trebuie sa inceapa cu litera mare.")
        if subiect and not subiect[0].isupper():
            raise ValidationError("Subiectul trebuie sa inceapa cu litera mare.")

        return cleaned_data

    def clean_mesaj(self):
        mesaj = self.cleaned_data.get('mesaj')
        mesaj = mesaj.replace('\n', ' ')
        mesaj = ' '.join(mesaj.split())
        
        cuvinte = len(mesaj.split())
        if cuvinte < 5 or cuvinte > 100:
            raise ValidationError("Mesajul trebuie sa contina intre 5 si 100 de cuvinte.")
        if 'http://' in mesaj or 'https://' in mesaj:
            raise ValidationError("Mesajul nu poate contine linkuri.")
        
        nume_utilizator = self.cleaned_data.get('nume')
        if not mesaj.endswith(nume_utilizator):
            raise ValidationError("Mesajul trebuie sa se termine cu semnatura (numele utilizatorului).")
        
        return mesaj

    def clean_data_nasterii(self):
        data_nasterii = self.cleaned_data.get('data_nasterii')
        if data_nasterii:
            today = datetime.today()
            years = today.year - data_nasterii.year
            months = today.month - data_nasterii.month
            if months < 0:
                years -= 1
                months += 12
            if years < 18:
                raise ValidationError("Expeditorul mesajului trebuie sa fie major.")
        
            return f"{years} ani si {months} luni"
        return data_nasterii
    
class PizzaForm(forms.ModelForm):
    discount = forms.DecimalField(label="Discount (%)", required=False, min_value=0, max_value=100, decimal_places=2)
    calorii = forms.IntegerField(label="Calorii", required=True, min_value=0, max_value=10000)

    class Meta:
        model = Pizza
        fields = ['nume', 'pret', 'gramaj', 'meniu']

        labels = {
            'nume': 'Denumire Pizza',
            'pret': 'Pret',
            'gramaj': 'Gramaj (g)',
            'meniu': 'Meniu'
        }
        help_texts = {
            'nume': 'Introduceti un nume scurt si descriptiv pentru pizza.',
            'pret': 'Pretul este exprimat in RON.',
        }

    def clean_discount(self):
        discount = self.cleaned_data.get('discount')
        if discount is not None and discount > 50:
            raise ValidationError("Discountul nu poate depasi 50%.")
        return discount

    def clean(self):
        cleaned_data = super().clean()
        pret = cleaned_data.get('pret')
        gramaj = cleaned_data.get('gramaj')
        discount = cleaned_data.get('discount')

        if pret is not None and gramaj is not None:
            if pret < gramaj / 50:
                raise ValidationError("Pretul trebuie sa fie cel putin 2% din gramaj.")
        
        if discount is not None and pret is not None:
            pret_final = pret - (pret * discount / 100)
            if pret_final < 1:
                raise ValidationError("Pretul final nu poate fi mai mic de 1 RON dupa aplicarea discountului.")

        return cleaned_data

    def clean_calorii(self):
        calorii = self.cleaned_data.get('calorii')
        if calorii is not None and calorii < 0:
            raise ValidationError("Numarul de calorii nu poate fi negativ.")
        return calorii
    
'''def trimite_mail():
    context = {'nume': 'Ionel'}  
    html_content = render_to_string('email_template.html', context)

    email = EmailMessage(
        subject='Salutare!',
        body=html_content,
        from_email='sebim5764@gmail.com',
        to=['sebim5764@gmail.com'],
    )
    email.content_subtype = 'html'
    email.send(fail_silently=False)'''
    
def trimite_mail_confirmare(user):
    cod_confirmare = user.cod
    context = {
        'username': user.username,  
        'oras': user.oras,
        'link_confirmare': f"http://localhost:8000/aplicatie_exemplu/confirma_mail/{user.cod}"
    }
    html_content = render_to_string('email_template.html', context)
    email = EmailMessage(
        subject='Confirmare inregistrare',
        body=html_content,
        from_email='sebim5764@gmail.com',
        to=[user.email],
    )
    email.content_subtype = 'html'
    email.send(fail_silently=False)


    
class CustomUserCreationForm(UserCreationForm):
    telefon = forms.CharField(required=True)
    data_nasterii = forms.DateField(required=True, widget = forms.DateInput(attrs={'type': 'date'}),)
    adresa = forms.CharField(required=True, max_length=255)
    oras = forms.CharField(required=True, max_length=100)
    newsletter = forms.BooleanField(
        required=False,
        initial=False,
        label="Doresc sa ma abonez la newsletter"
    )

    class Meta:
        model = CustomUser
        fields = ("username","email", "telefon", "data_nasterii", "adresa", "oras", "newsletter", "password1", "password2")
        
    def clean_telefon(self):
        telefon = self.cleaned_data.get('telefon')
        if not telefon.isdigit():
            raise ValidationError("Numarul de telefon trebuie sa contina doar cifre")
        if len(telefon) != 10:
            raise ValidationError("Numarul de telefon trebuie sa contina 10 cifre")
        return telefon
    
    def clean_data_nasterii(self):
        data_nasterii = self.cleaned_data.get('data_nasterii')
        if data_nasterii > datetime.date.today():
            raise ValidationError("Data nasterii este incorecta")
        return data_nasterii
    

    def clean_oras(self):
        oras = self.cleaned_data.get('oras')
        if not re.match(r'^[a-zA-Z\s\-]+$', oras):
            raise ValidationError("Numele orasului poate contine doar litere, spatii si cratime.")
        return oras

        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.telefon = self.cleaned_data["telefon"]
        user.data_nasterii = self.cleaned_data["data_nasterii"]
        user.adresa = self.cleaned_data["adresa"]
        user.oras = self.cleaned_data["oras"]
        user.newsletter = self.cleaned_data["newsletter"]
        user.cod = str(uuid.uuid4())
        if commit:
            trimite_mail_confirmare(user)
            user.save()
        return user

class CustomAuthenticationForm(AuthenticationForm):
    ramane_logat = forms.BooleanField(
        required=False,
        initial=False,
        label='Ramaneti logat'
    )
    
    def confirm_login_allowed(self, user):
        if not user.email_confirmat:
            raise ValidationError(
                "Emailul nu a fost confirmat. Te rugam sa confirmi adresa de email.",
                code='email_not_confirmed',
            )
        super().confirm_login_allowed(user)
