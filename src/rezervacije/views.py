from datetime import date, timedelta
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import (
	Exists,
	OuterRef,
	Q,
	)
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.dateparse import parse_date

from .forms import RezervirajForm
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
	sve_rez = Rezervacija.objects.filter(korisnik__id = gost.id)
	danas2 = date.today()
	for jedna in sve_rez:
		if jedna.datum_rezervacije < danas2:
			jedna.delete()
	nove_rez = Rezervacija.objects.filter(korisnik__id = gost.id)
	br_rez = nove_rez.count()

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

	eend = ee3 - 1
	bbeg = bb3 + 1

	korisnik = request.user

	if bb3 >= ee3:
		return redirect('greska')
	if bb3 < 8 or bb3 > 22:
		return redirect('greska')
	if ee3 < 9 or ee3 > 23:
		return redirect('greska')

	grad = Lokacija.objects.get(id = grad_kljuc)
	datum_rez = parse_date(datum_string)

	svi_stolovi = Stol.objects.filter(lokacija__id = grad_kljuc, broj_stolica = br_stolica)

	izbaci_ga_zajedno = Rezervacija.objects.filter(Q(kraj_rezervacije__range = (bbeg, ee3)) | Q(pocetak_rezervacije__range = (bb3, eend)), datum_rezervacije = datum_rez)
	izbaci_qs = izbaci_ga_zajedno.count()
	izbaci_ga = Rezervacija.objects.filter(Q(kraj_rezervacije__range = (bbeg, ee3)) | Q(pocetak_rezervacije__range = (bb3, eend)), datum_rezervacije = datum_rez).values_list('stol_id', flat=True)

	izbaci_ga2_zajedno = Rezervacija.objects.filter(Q(kraj_rezervacije__gt = ee3) & Q(pocetak_rezervacije__lt = bb3), datum_rezervacije = datum_rez)
	izbaci_ga2_qs = izbaci_ga2_zajedno.count()
	izbaci_ga2 = Rezervacija.objects.filter(Q(kraj_rezervacije__gt = ee3) & Q(pocetak_rezervacije__lt = bb3), datum_rezervacije = datum_rez).values_list('stol_id', flat=True)

	if izbaci_qs > 0:
		prvi_qs = svi_stolovi.exclude(id__in = izbaci_ga)
	else:
		prvi_qs = svi_stolovi

	if izbaci_ga2_qs > 0:
		prvi_qs = prvi_qs.exclude(id__in = izbaci_ga2)

	rezer2 = Rezervacija.objects.filter(
		stol = OuterRef('pk'),
		datum_rezervacije = datum_rez,
		)
	drugi_qs = Stol.objects.annotate(nepostoji = Exists(rezer2)).filter(nepostoji = False, lokacija__id = grad_kljuc, broj_stolica = br_stolica)

	zajedno_qs = prvi_qs | drugi_qs

	pravi_qs = zajedno_qs.order_by('broj_stola')
	pravi_qs = pravi_qs.distinct()
	zbroj_qs = zajedno_qs.count()

	context = {"tittle": tittle,"datum_rez": datum_rez,
	"br_stolica": br_stolica,"poc":poc,"kraj": kraj,
	"grad": grad,"pravi_qs":pravi_qs,"zbroj_qs": zbroj_qs,
	}
	return render(request, template_name, context)


@login_required
def zadnja_rezervacija_view(request):
	tittle = 'Zadnja'
	datum_text = request.POST.get('post_datum2', None)
	#stolice = request.POST.get('post_stolice2', None)
	pocetak = request.POST.get('post_pocetak2', None)
	krajj = request.POST.get('post_kraj2', None)
	#za_kljuc_grada = request.POST.get('post_id_grada2', None)
	za_stola = request.POST.get('post_id_stola', None)
	if datum_text == None or pocetak == None or krajj == None or za_stola == None:
		return redirect('greska')

	korisnik = request.user

	end1 = krajj
	beg1 = pocetak
	end2 = str(end1)
	beg2 = str(beg1)
	end3 = int(end2)
	beg3 = int(beg2)

	if beg3 < 8 or beg3 > 22:
		return redirect('greska')
	if end3 < 9 or end3 > 23:
		return redirect('greska')

	if end3 > beg3:
		if request.method == "POST":
			form = RezervirajForm(request.POST)
			if form.is_valid():
				datum_rezervacije99 = form.cleaned_data.get('post_datum2')
				promjeni_datum = parse_date(datum_rezervacije99)
				uhvati_stol_kljuc = form.cleaned_data.get('post_id_stola')
				uhvati_stol = get_object_or_404(Stol, id = uhvati_stol_kljuc)

				rezervacije_kor = Rezervacija.objects.filter(korisnik = korisnik)
				broji_rez = rezervacije_kor.count()
				if broji_rez > 2:
					messages.warning(request, ('Mozete maksimalno imati tri rezervacije.'))
					return redirect('home')

				ako_postoji = Rezervacija.objects.filter(
					stol = uhvati_stol,
					datum_rezervacije = promjeni_datum,
					pocetak_rezervacije = form.cleaned_data.get('post_pocetak2'),
					kraj_rezervacije = form.cleaned_data.get('post_kraj2')
					)
				ako_postoji_broj = ako_postoji.count()
				if ako_postoji_broj > 0:
					return redirect('greska')

				kreiranje_rez = Rezervacija.objects.create(
					korisnik = korisnik,
					stol = uhvati_stol,
					datum_rezervacije = promjeni_datum,
					pocetak_rezervacije = form.cleaned_data.get('post_pocetak2'),
					kraj_rezervacije = form.cleaned_data.get('post_kraj2')
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


@staff_member_required
def arhiviraj_view(request):
	sve_rezervacije = Rezervacija.objects.all()
	danas3 = date.today()
	for jedno in sve_rezervacije:
		if jedno.datum_rezervacije < danas3:
			jedno.delete()
	messages.success(request, ('Istekle rezervacije su uspjesno obrisane!'))
	return redirect('profil')