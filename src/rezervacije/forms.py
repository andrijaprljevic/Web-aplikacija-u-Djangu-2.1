from django import forms

class PrvaForm(forms.Form):
	datum_rezervacije = forms.DateField(input_formats=('%Y-%m-%d'))
	broj_stolica = forms.IntegerField(max_value = 8, min_value = 2)
	pocetak_rezervacije = forms.IntegerField(max_value = 22, min_value = 8)
	kraj_rezervacije = forms.IntegerField(max_value = 23, min_value = 9)
	id_grada = forms.IntegerField()

class DrugaForm(forms.Form):
	datum_rezervacije = forms.DateField(input_formats=('%Y-%m-%d'))
	pocetak_rezervacije = forms.IntegerField(max_value = 22, min_value = 8)
	kraj_rezervacije = forms.IntegerField(max_value = 23, min_value = 9)
	id_stola = forms.IntegerField()
