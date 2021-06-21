from django.db import models
from django.core.validators import MinLengthValidator

class Make(models.Model):
    name=models.CharField(max_length=100, help_text='Enter an item',
    validators=[MinLengthValidator(2, 'Mínimo dos carácteres por favor')])
    def __str__(self):
        return self.name


class Auto(models.Model):
    nickname=models.CharField(max_length=100, validators=[MinLengthValidator(2, 'El nombre como mínimo debe tener dos letras')])
    mileage=models.PositiveIntegerField()
    comments=models.CharField(max_length=100)
    make=models.ForeignKey('Make', on_delete=models.CASCADE,null=False)
    def __str__(self):
        return self.nickname