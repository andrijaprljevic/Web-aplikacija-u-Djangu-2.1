from django.contrib import admin

from .models import Jelovnik

# Register your models here.


class JelovnikAdmin(admin.ModelAdmin):
	list_display = ('naziv', 'id', 'vrsta', 'cijena', 'sastojci', 'dnevna_ponuda')
	ordering = ('dnevna_ponuda', 'vrsta', 'naziv',)
	search_fields = ('naziv', 'vrsta',)
	readonly_fields = ('id',)

admin.site.register(Jelovnik, JelovnikAdmin)