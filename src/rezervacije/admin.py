from django.contrib import admin

from .models import (
	Lokacija,
	Stol,
	Rezervacija,
)

# Register your models here.




class LokacijaAdmin(admin.ModelAdmin):
	list_display = ('ime_grada', 'id', 'adresa_restorana')
	ordering = ('ime_grada',)
	search_fields = ('ime_grada',)
	readonly_fields = ('id',)

class StolAdmin(admin.ModelAdmin):
	list_display = ('broj_stola', 'broj_stolica', 'lokacija', 'id')
	ordering = ('broj_stola',)
	search_fields = ('broj_stolica', 'lokacija__ime_grada',)
	readonly_fields = ('id',)
#	def grad(self, instance):
#        return instance.lokacija.ime_grada

class RezervacijaAdmin(admin.ModelAdmin):
	list_display = ('korisnik','datum_rezervacije', 'pocetak_rezervacije', 'kraj_rezervacije', 'stol', 'id', 'timestamp')
	ordering = ('timestamp',)
	search_fields = ('korisnik__username', 'stol__lokacija__ime_grada', 'datum_rezervacije',)
	readonly_fields = ('id',)

admin.site.register(Lokacija, LokacijaAdmin)
admin.site.register(Stol, StolAdmin)
admin.site.register(Rezervacija, RezervacijaAdmin)