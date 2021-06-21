from django import forms
from .models import Ad
from ads.humanize import naturalsize
from django.core.files.uploadedfile import InMemoryUploadedFile

# Creamos la clase formulario
class CreateAd(forms.ModelForm):
    # creamos las variables del espacio. Un MB contiene 1024 kilobytes
    # un KB contiene 1024 bytes. Por tanto 2MB=2*1024*1024
    max_upload_limit=2*1024*1024
    max_upload_limit_text=naturalsize(max_upload_limit)

    # cambiamos el field asociado a picture, de forma que lo llamaremos
    # igual para que cuando lo salvemos se guarde en el campo del modelo
    picture=forms.FileField(required=False, label='File to Upload max size:'+max_upload_limit_text)
    # el campo que sigue, es para especificar el campo en el que se va a cargar un archivo
    # precisamente upload_field_name se usa en el script de java en el html
    upload_field_name='picture'

    class Meta:
        model=Ad
        fields = ['title', 'text', 'price', 'picture']  # Picture is manual

    # Validate the size of the picture
    def clean(self):
        cleaned_data = super().clean()
        pic = cleaned_data.get('picture')
        if pic is None:
            return
        if len(pic) > self.max_upload_limit:
            self.add_error('picture', "File must be < "+self.max_upload_limit_text+" bytes")

    # Convert uploaded File object to a picture
    def save(self, commit=True):
        instance = super(CreateAd, self).save(commit=False)

        # We only need to adjust picture if it is a freshly uploaded file
        f = instance.picture   # Make a copy
        if isinstance(f, InMemoryUploadedFile):  # Extract data from the form to the model
            bytearr = f.read()
            instance.content_type = f.content_type
            instance.picture = bytearr  # Overwrite with the actual image data

        if commit:
            instance.save()

        return instance

# Creamos la clase comentario
class CommentForm(forms.Form):
    comment=forms.CharField(required=True, max_length=500, min_length=3, strip=True)