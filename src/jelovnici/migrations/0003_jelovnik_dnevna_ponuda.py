# Generated by Django 2.1 on 2019-09-12 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jelovnici', '0002_auto_20190912_2002'),
    ]

    operations = [
        migrations.AddField(
            model_name='jelovnik',
            name='dnevna_ponuda',
            field=models.BooleanField(default=False),
        ),
    ]
