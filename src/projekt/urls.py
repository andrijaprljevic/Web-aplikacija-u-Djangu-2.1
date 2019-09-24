"""projekt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path, include

from rezervacije.views import (
    prva_rezervacija_view,
    druga_rezervacija_view,
    zadnja_rezervacija_view,
    greska_view,
)
from profili.views import (
    login_view,
    register_view, 
    logout_view,
    azuriraj_view,
    profil_view,
    change_password_view,
    obrisi_rezervaciju_view,
    deaktiviraj_view,
)
from jelovnici.views import (
    home_view,
    o_nama_view,
    jelovnik_view,
    vina_view,
    detail_view,
    kontakt_view,
    )

urlpatterns = [
    path('admin/', admin.site.urls),

    path('registracija/', register_view, name ='registracija'),
    path('prijava/', login_view, name ='prijava'),
    path('odjava/', logout_view, name ='odjava'),
    path('profil/', profil_view, name ='profil'),
    path('azuriraj/', azuriraj_view, name ='azuriraj'),
    path('password/', change_password_view, name ='password'),
    path('deaktivacija/', deaktiviraj_view, name ='deaktiviraj'),
    path('obrisi_rezervaciju/', obrisi_rezervaciju_view, name ='obrisi_rezervaciju'),

    path('rezervacija/', prva_rezervacija_view, name ='prva'),
    path('odaberistol/', druga_rezervacija_view, name ='druga'),
    path('rezerviranje/', zadnja_rezervacija_view, name ='zadnja'),
    path('error/', greska_view, name ='greska'),

    path('o_nama/', o_nama_view, name ='o_nama'),
    path('jelovnik/', jelovnik_view, name ='jelovnik'),
    path('vina/', vina_view, name ='vina'),
    path('detalji/<int:post_id>', detail_view, name ='detalji'),
    path('kontakt/', kontakt_view, name ='kontakt'),
    path('', home_view, name ='home'),

    path('', include('sendemail.urls')),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)