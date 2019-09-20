from datetime import date, timedelta
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef, Q
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.dateparse import parse_date

#from .forms import PrvaForm, DrugaForm
from .models import (
	Lokacija,
	Stol,
	Rezervacija,
)
# Create your views here.


@login_required
def prva_rezervacija_view(request):
	template_name = 'rezervacije/rezervacija1.html'
	tittle = "Rezervacija stola"
	danas = date.today()
	sutra = danas + timedelta(days=1)
	dvamjeseca = danas + timedelta(days=60)
	sve_lokacije = Lokacija.objects.all()
	gost = request.user
	br_rez = Rezervacija.objects.filter(korisnik__id = gost.id).count()

	context = {"danas": danas,"tittle": tittle,
	"sutra": sutra,"dvamjeseca": dvamjeseca,
	"sve_lokacije": sve_lokacije, "br_rez": br_rez
	}
	return render(request, template_name, context)


@login_required
def druga_rezervacija_view(request):
	template_name = 'rezervacije/rezervacija2.html'
	tittle = "Odabir stola"
	datum_string = request.POST.get('post_datum', None)
	br_stolica = request.POST.get('post_stolice', None)
	poc = request.POST.get('post_pocetak', None)
	kraj = request.POST.get('post_kraj', None)
	grad_kljuc = request.POST.get('post_id_grada', None)
	if datum_string == None or br_stolica == None or poc == None or kraj == None or grad_kljuc == None:
		return redirect('greska')
	
	ee1 = kraj
	bb1 = poc
	ee2 = str(ee1)
	bb2 = str(bb1)
	ee3 = int(ee2)
	bb3 = int(bb2)

	if bb3 >= ee3:
		return redirect('greska')

	grad = Lokacija.objects.get(id = grad_kljuc)
	datum_rez = parse_date(datum_string)

	rezer1 = Rezervacija.objects.filter(
		Q(kraj_rezervacije__lte = poc) | Q(pocetak_rezervacije__gte = kraj),
		stol = OuterRef('pk'),
		datum_rezervacije = datum_rez,
		)
	rezer2 = Rezervacija.objects.filter(
		stol = OuterRef('pk'),
		datum_rezervacije = datum_rez,
		)
	prvi_qs = Stol.objects.annotate(postoji = Exists(rezer1)).filter(postoji = True, lokacija__id = grad_kljuc, broj_stolica = br_stolica)
	drugi_qs = Stol.objects.annotate(nepostoji = Exists(rezer2)).filter(nepostoji = False, lokacija__id = grad_kljuc, broj_stolica = br_stolica)
	zajedno_qs = prvi_qs | drugi_qs
	pravi_qs = zajedno_qs.order_by('broj_stola')
	zbroj_qs = pravi_qs.count()

	context = {"tittle": tittle,"datum_rez": datum_rez,
	"br_stolica": br_stolica,"poc":poc,"kraj": kraj,
	"grad": grad,"pravi_qs":pravi_qs,"zbroj_qs": zbroj_qs,
	}
	return render(request, template_name, context)


@login_required
def zadnja_rezervacija_view(request):
	tittle = 'Zadnja'
	datum_text = request.POST.get('post_datum2', None)
	stolice = request.POST.get('post_stolice2', None)
	pocetak = request.POST.get('post_pocetak2', None)
	krajj = request.POST.get('post_kraj2', None)
	za_kljuc_grada = request.POST.get('post_id_grada2', None)
	za_stola = request.POST.get('post_id_stola', None)
	if datum_text == None or stolice == None or pocetak == None or krajj == None or za_kljuc_grada == None or za_stola == None:
		return redirect('greska')

	pravi_datum = parse_date(datum_text)
	location = Lokacija.objects.get(id = za_kljuc_grada)
	pravi_stol = Stol.objects.get(id = za_stola)
	korisnik = request.user

	end1 = krajj
	beg1 = pocetak
	end2 = str(end1)
	beg2 = str(beg1)
	end3 = int(end2)
	beg3 = int(beg2)

	if end3 > beg3:
		ako_postoji = Rezervacija.objects.filter(
			korisnik = korisnik,
			datum_rezervacije = pravi_datum,
			pocetak_rezervacije = pocetak,
			kraj_rezervacije = krajj
			)
		ako_postoji_broj = ako_postoji.count()
		if ako_postoji_broj > 0:
			return redirect('greska')
		else:
			kreiranje_rez = Rezervacija.objects.create(
				korisnik = korisnik,
				stol = pravi_stol,
				datum_rezervacije = pravi_datum,
				pocetak_rezervacije = pocetak,
				kraj_rezervacije = krajj
				)
			messages.success(request, ('Rezervacija je uspjela!'))
			return redirect('profil')

	return redirect('greska')


@login_required
def greska_view(request):
	template_name = 'rezervacije/greska.html'
	tittle = 'Error'
	context = {"tittle": tittle}
	return render(request, template_name, context)
	




def test_view(request):
	template_name = 'test.html'
	obj1 = get_object_or_404(Rezervacija, id = 1)
	obj2 = get_object_or_404(Rezervacija, id = 2)
	obj_stol_br = get_object_or_404(Rezervacija, stol__broj_stola = 18)
	mostarski = Rezervacija.objects.filter(stol__lokacija__ime_grada__iexact = 'mostar')
	siroki = Rezervacija.objects.filter(stol__lokacija__ime_grada__icontains = 'brijeg')
	danas = date.today()
	sutra = danas + timedelta(days=1)
	mjesec = danas + timedelta(days=60)

	primjer = danas

	#primjer.strftime('%Y-X%m-X%d').replace('X0','X').replace('X','')

	mostarski_i_siroki = mostarski | siroki
	m_i_s = mostarski_i_siroki.order_by('-stol__broj_stola')

	#d = date(2019-9-18)
	datum_rezervacije2 = request.POST.get('datum_rezervacije')
	datum_rezervacijehahaha = parse_date(datum_rezervacije2)
	#datum_rezervacije.strftime('%Y-X%m-X%d').replace('X0','X').replace('X','')

	p = 18
	k = 20
	st = 2
	stolhh = Stol.objects.filter(broj_stolica = st, lokacija__ime_grada__icontains = 'siroki').first()
	korisnik = request.user

	kreiranje = Rezervacija.objects.create(
		korisnik = korisnik,
		stol = stolhh,
		datum_rezervacije = datum_rezervacijehahaha,
		pocetak_rezervacije = p,
		kraj_rezervacije = k
		)

	context = {"ob1": obj1, "ob2": obj2, "dan": danas, 
				"sutra": sutra, "mjesec": mjesec, 
				"objekt": obj_stol_br, "mostarski": mostarski, 
				"siroki": siroki, "m_i_s": m_i_s,
				"bez_nule": primjer, "datum_rezervacije": datum_rezervacijehahaha
				}

	return render(request, template_name, context)



def test2_view(request):
	template_name = 'test2.html'
	obj1 = get_object_or_404(Rezervacija, id = 1)
	obj2 = get_object_or_404(Rezervacija, id = 2)
	obj_stol_br = get_object_or_404(Rezervacija, stol__broj_stola = 18)
	mostarski = Rezervacija.objects.filter(stol__lokacija__ime_grada__iexact = 'mostar')
	siroki = Rezervacija.objects.filter(stol__lokacija__ime_grada__icontains = 'brijeg')
	danas = date.today()
	sutra = danas + timedelta(days=1)
	mjesec = danas + timedelta(days=60)

	primjer = danas

	#primjer.strftime('%Y-X%m-X%d').replace('X0','X').replace('X','')

	mostarski_i_siroki = mostarski | siroki
	m_i_s = mostarski_i_siroki.order_by('-stol__broj_stola')

	#d = date(2019-9-18)
	p = 18
	k = 20
	st = 6



	context = {"ob1": obj1, "ob2": obj2, "dan": danas, 
				"sutra": sutra, "mjesec": mjesec, 
				"objekt": obj_stol_br, "mostarski": mostarski, 
				"siroki": siroki, "m_i_s": m_i_s,
				"bez_nule": primjer
				}

	return render(request, template_name, context)