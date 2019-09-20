from django.db import models

# Create your models here.

class Jelovnik(models.Model):
	naziv			=	models.CharField(max_length=45)
	vrsta			=	models.CharField(max_length=45)
	cijena			=	models.CharField(max_length=45, null=True, blank=True)
	sastojci		=	models.CharField(max_length=200, null=True, blank=True)
	dnevna_ponuda	=	models.BooleanField(default=False)
	image			=	models.FileField(upload_to='image/', null=True, blank=True)
	def __str__(self):
		return self.naziv + ' - ' + self. vrsta
	class Meta:
		verbose_name_plural = "Jelovnik"