from django import forms

class ContactForm(forms.Form):
	from_email = forms.EmailField(required=True, label=("Vas email"))
	subject = forms.CharField(required=True, label=("Tema"))
	message = forms.CharField(widget=forms.Textarea, required=True, label=("Poruka"))