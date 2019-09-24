from django.shortcuts import render, get_object_or_404, redirect

from .models import Jelovnik
from rezervacije.models import Lokacija
# Create your views here.

def home_view(request):
	tittle = "Restoran Maslina"
	qs_sve = Jelovnik.objects.filter(dnevna_ponuda = True)
	context = {
		'qs_sve': qs_sve,
		'tittle': tittle,
	}
	return render(request, 'home.html', context)

def o_nama_view(request):
	tittle = "O nama"
	context = {
		'tittle': tittle,
	}
	return render(request, 'o_nama.html', context)

def jelovnik_view(request):
	tittle = "Jelovnik"
	qs_mesna1 = Jelovnik.objects.filter(vrsta__icontains = 'mesna')
	qs_mesna = qs_mesna1.order_by('naziv')
	qs_pizza1 = Jelovnik.objects.filter(vrsta__icontains = 'pizza')
	qs_pizza = qs_pizza1.order_by('naziv')
	qs_rizota1 = Jelovnik.objects.filter(vrsta__icontains = 'rizot')
	qs_rizota = qs_rizota1.order_by('naziv')
	qs_salate1 = Jelovnik.objects.filter(vrsta__icontains = 'salat')
	qs_salate = qs_salate1.order_by('naziv')
	context = {
		'qs_mesna': qs_mesna,
		'qs_pizza': qs_pizza,
		'qs_rizota': qs_rizota,
		'qs_salate': qs_salate,
		'tittle': tittle,
	}
	return render(request, 'jelovnik.html', context)

def vina_view(request):
	tittle = "Vina"
	qs_vina = Jelovnik.objects.filter(vrsta__icontains = 'vino')
	context = {
		'qs_vina': qs_vina,
		'tittle': tittle,
	}
	return render(request, 'vina.html', context)

def detail_view(request, post_id):
	object_detalj = get_object_or_404(Jelovnik, id = post_id)
	tittle = object_detalj.naziv
	context = {
		'object_detalj': object_detalj,
		'tittle': tittle,
	}
	return render(request, 'detalji.html', context)


def kontakt_view(request):
	tittle = "Informacije i Kontakt"
	qs_gradovi = Lokacija.objects.all()
	context = {
		'qs_gradovi': qs_gradovi,
		'tittle': tittle,
	}
	return render(request, 'informacije.html', context)