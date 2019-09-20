from django import forms
from django.contrib.auth import (
	authenticate,
	get_user_model,
	login,
	logout,
	)
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, ReadOnlyPasswordHashField
from django.contrib.auth.models import User

Korisnik = get_user_model()

class LoginForm(forms.Form):
	username = forms.CharField(required = True, label=("Username"))
	password = forms.CharField(required = True, label=("Lozinka"), widget=forms.PasswordInput)

	def clean(self, *args, **kwargs):
		username = self.cleaned_data.get("username")
		password = self.cleaned_data.get("password")
		if username and password:
			user = authenticate(username=username, password=password)
			if not user:
				raise forms.ValidationError("Ovaj korisnik ne postoji, ili je deaktiviran.")
			if not user.check_password(password):
				raise forms.ValidationError("Lozinka nije točna.")
			if not user.is_active:
				raise forms.ValidationError("Ovaj korisnik nije aktivan.")
		return super(LoginForm, self).clean(*args, **kwargs)



class RegistrationForm(UserCreationForm):
	error_messages = {
		'password_mismatch': ("Lozinke se ne podudaraju."),
	}
	email = forms.EmailField(required = True)
	password1 = forms.CharField(
		label=("Lozinka"),
		strip=False,
		widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
	)
	password2 = forms.CharField(
		label=("Potvrdi lozinku"),
		widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
		strip=False,
	)

	def __init__(self, *args, **kwargs):
		super(RegistrationForm, self).__init__(*args, **kwargs)

		for fieldname in ['username', 'password1', 'password2']:
			self.fields[fieldname].help_text = None

	class Meta:
		model = User
		fields = [
			'username',
			'email',
			'password1',
			'password2'
		]

	def clean_username(self):
		username = self.cleaned_data.get('username')
		qs1 = User.objects.filter(username__iexact=username)
		if qs1.exists():
			raise forms.ValidationError("Ovo korisnicko ime vec postoji. Izaberite drugo korisnicko ime.")
		return username

	def clean_email(self):
		email = self.cleaned_data.get('email')
		qs = User.objects.filter(email__iexact=email)
		if qs.exists():
			raise forms.ValidationError("Ovaj email vec postoji. Izaberite drugi email.")
		return email

	def save(self, commit = True):
		user = super(RegistrationForm, self).save(commit = False)
		user.is_active = True

		if commit:
			user.save()

		return user


class UpdateForm(UserChangeForm):
	password = ReadOnlyPasswordHashField(
		label=("Lozinka"),
		help_text=(
			'Lozinke se samo u obliku hasha spremaju u bazu podataka, tako da se ne može vidjeti '
			'lozinka ovog korisnika, ali lozinku možete promjeniti koristeći '
			'<a href="{}"><b>OVU FORMU</b></a>.'
		),
	)

	class Meta:
		model = User
		fields = (
			'first_name',
			'last_name',
			'password'
			)