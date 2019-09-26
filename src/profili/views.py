from datetime import date, timedelta
from django.contrib import messages
from django.contrib.auth import (
	authenticate,
	get_user_model,
	login,
	logout,
	)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404

from rezervacije.models import (
	Lokacija,
	Stol,
	Rezervacija,
)

from .forms import (
	LoginForm,
	RegistrationForm,
	UpdateForm,
	)
# Create your views here.

def login_view(request):
	tittle = "Prijava"
	if request.user.is_authenticated:
		messages.warning(request, ('Vec ste prijavljeni.'))
		return redirect('home')
	form = LoginForm(request.POST or None)
	if form.is_valid():
		username = form.cleaned_data.get("username")
		password = form.cleaned_data.get("password")
		user = authenticate(username=username, password=password)
		login(request, user)
		return redirect('home')
	return render(request, 'profili/prijava.html', {"form": form, 'tittle': tittle})

def register_view(request):
	tittle = "Registracija"
	if request.user.is_authenticated:
		messages.warning(request, ('Vec ste registrirani.'))
		return redirect('home')
	if request.method == 'POST':
		form = RegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('prijava')
	else:
		form = RegistrationForm()
	return render(request, 'profili/registracija.html', {'form': form, 'tittle': tittle})

def logout_view(request):
	logout(request)
	return redirect('home')

@login_required
def azuriraj_view(request):
	tittle = "Ažuriranje profila"
	if request.method == 'POST':
		form = UpdateForm(request.POST, instance=request.user)
		if form.is_valid():
			form.save()
			return redirect('profil')
	else:
		form = UpdateForm(instance=request.user)
	return render(request, 'profili/azuriraj.html', {'form': form, 'tittle': tittle})

@login_required
def profil_view(request):
	tittle = 'Profil'

	kor = request.user
	sve_rez = Rezervacija.objects.filter(korisnik__id = kor.id)
	danas2 = date.today()
	for jedna in sve_rez:
		if jedna.datum_rezervacije < danas2:
			jedna.delete()
	rez_kor1 = Rezervacija.objects.filter(korisnik = kor)
	rez_kor = rez_kor1.order_by('datum_rezervacije', 'pocetak_rezervacije')
	rez_br = rez_kor.count()

	context = {
	"tittle": tittle, "rez_kor": rez_kor,
	"rez_br": rez_br,
	}
	return render(request, 'profili/profil.html', context)


@login_required
def change_password_view(request):
	tittle = 'Promjena Lozinke'
	if request.method == 'POST':
		form = PasswordChangeForm(data=request.POST, user=request.user)

		if form.is_valid():
			form.save()
			return redirect('prijava')
	else:
		form = PasswordChangeForm(user=request.user)

		return render(request, 'profili/change_password.html', {'form': form, 'tittle': tittle})



@login_required
def obrisi_rezervaciju_view(request):
	kljuc_od_rezervacije = request.POST.get('kljuc_rezervacije', None)
	if kljuc_od_rezervacije == None:
		return redirect('odjava')

	creator = request.user
	qs_izbrisi_rezervaciju = get_object_or_404(Rezervacija, id = kljuc_od_rezervacije)
	danas1 = date.today()
	if qs_izbrisi_rezervaciju.korisnik == creator:
		if qs_izbrisi_rezervaciju.datum_rezervacije == danas1:
			messages.success(request, ('Ne možete više obrisati rezervaciju.'))
			return redirect('profil')
		else:
			qs_izbrisi_rezervaciju.delete()
			messages.success(request, ('Rezervacija je uspjesno obrisana!'))
			return redirect('profil')

	return redirect('greska')



def deaktiviraj_view(request):
	if request.user.is_authenticated:
		koris = request.user
		rez_koris = Rezervacija.objects.filter(korisnik = koris)
		rez_koris.delete()
		koris.is_active = False
		koris.save()
		logout(request)
		messages.success(request, ('Profil je uspjesno deaktiviran!'))
		return redirect('home')
	else:
		messages.warning(request, ('Niste prijavljeni.'))
	return redirect('home')

