from django.shortcuts import render
from django.contrib import messages

# Create your views here.

from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

from .forms import ContactForm


def emailView(request):
	tittle = 'Kontaktirajte nas'
	if request.method == 'GET':
		form = ContactForm()
	else:
		form = ContactForm(request.POST)
		if form.is_valid():
			subject = form.cleaned_data['subject']
			from_email = form.cleaned_data['from_email']
			message = form.cleaned_data['message']
			try:
				send_mail(subject, message, from_email, ['admin@example.com'])
			except BadHeaderError:
				return redirect('greska')
			messages.success(request, ('Uspjesno the poslali poruku!'))
			return redirect('home')
	return render(request, "email.html", {'form': form, 'tittle': tittle})

def successView(request):
	return HttpResponse('Success! Thank you for your message.')