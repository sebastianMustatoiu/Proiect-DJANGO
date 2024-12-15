from django.contrib import admin
from .models import Meniu, Pizza, Ingredient, Comanda, Ambalaj

class MeniuAdmin(admin.ModelAdmin):
    search_fields = ('nume', 'data_creare')
    
class IngredientAdmin(admin.ModelAdmin):
    search_fields = ('nume', 'calorii')
    
class AmbalajAdmin(admin.ModelAdmin):
    search_fields = ('nume', 'material')
    
class ComandaAdmin(admin.ModelAdmin):
    search_fields = ('nume_client', 'id_comanda')

class PizzaAdmin(admin.ModelAdmin):
    list_display = ('nume', 'pret', 'gramaj', 'descriere', 'meniu', 'ambalaj')
    list_filter = ('nume', 'pret')
    search_fields = ('nume', 'pret')
    fieldsets = (
        ('Informatii Generale', {
            'fields': ('nume', 'descriere')
        }),
        ('Date', {
            'fields' : ('pret', 'gramaj')
        }),
        ('Alte date', {
            'fields' : ('meniu', 'ambalaj'),
            'classes' : ('collapse', ),
        })
    )

admin.site.register(Meniu, MeniuAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Comanda, ComandaAdmin)
admin.site.register(Pizza, PizzaAdmin)
admin.site.register(Ambalaj, AmbalajAdmin)

admin.site.site_header = "Panou de Administrare Site Pizza"
admin.site.site_title = "Admin Site"
admin.site.index_title = "Bine ai venit în panoul de administrare"