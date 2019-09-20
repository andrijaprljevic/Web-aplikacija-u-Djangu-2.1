from django.conf import settings
from django.db import models

# Create your models here.

User = settings.AUTH_USER_MODEL

class Lokacija(models.Model):
	ime_grada			=	models.CharField(max_length=45)
	adresa_restorana	=	models.CharField(max_length=100)
	def __str__(self):
		return self.ime_grada
	class Meta:
		verbose_name_plural = "Lokacije"

class Stol(models.Model):
	lokacija		=	models.ForeignKey(Lokacija, on_delete=models.CASCADE)
	broj_stola		=	models.IntegerField()
	broj_stolica	=	models.IntegerField()
	def __str__(self):
		#return ('Stol: ' + str(self.broj_stola) + ' --- Broj Stolica: ' + str(self.broj_stolica) + ' --- Grad: ' + self.lokacija.ime_grada)
		#return self.lokacija.ime_grada
		return ('Stol: ' + str(self.broj_stola) + ' - Br. Stolica: ' + str(self.broj_stolica) + ' - Grad: ' + self.lokacija.ime_grada)
	class Meta:
		verbose_name_plural = "Stolovi"

class Rezervacija(models.Model):
	korisnik			=	models.ForeignKey(User, on_delete=models.CASCADE)
	stol				=	models.ForeignKey(Stol, on_delete=models.CASCADE)
	datum_rezervacije	=	models.DateField(auto_now=False, auto_now_add=False, null=False, blank=False)
	pocetak_rezervacije	=	models.IntegerField()
	kraj_rezervacije	=	models.IntegerField()
	timestamp			=	models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return self.korisnik.username
	class Meta:
		verbose_name_plural = "Rezervacije"