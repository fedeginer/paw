# Generated by Django 3.1.4 on 2021-01-25 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unesco', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='site',
            name='area_hectares',
            field=models.FloatField(null=True),
        ),
    ]