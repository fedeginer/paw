# Generated by Django 3.1.4 on 2021-01-08 22:15

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Make',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Este mensaje acompaña al formulario', max_length=100, validators=[django.core.validators.MinLengthValidator(2, 'Mínimo dos carácteres por favor')])),
            ],
        ),
        migrations.CreateModel(
            name='Auto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(max_length=100, validators=[django.core.validators.MinLengthValidator(2, 'El nombre como mínimo debe tener dos letras')])),
                ('mileage', models.CharField(max_length=100)),
                ('comments', models.CharField(max_length=100)),
                ('make', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='autos.make')),
            ],
        ),
    ]
