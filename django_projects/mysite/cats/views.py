from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Cat, Breed
from django.urls import reverse_lazy

class CatsIndex(LoginRequiredMixin, View):
    template='cats/catlist.html'
    def get(self, request):
        cats=Cat.objects.all()
        count=Breed.objects.all().count()
        return render(request, self.template,{'cats':cats, 'count':count})

# ojo porque trabaja con pk, no con id
class UpdateCat(LoginRequiredMixin, UpdateView):
    model=Cat
    fields='__all__'
    success_url=reverse_lazy('cats:index')

class DeleteCat(LoginRequiredMixin, DeleteView):
    model=Cat
    fields='__all__'
    success_url=reverse_lazy('cats:index')

class CreateCat(LoginRequiredMixin, CreateView):
    model=Cat
    fields='__all__'
    success_url=reverse_lazy('cats:index')

class BreedList(LoginRequiredMixin, View):
    template='cats/breedlist.html'
    def get(self,request):
        breeds=Breed.objects.all()
        return render(request, self.template, {'breeds':breeds})

class CreateBreed(LoginRequiredMixin, CreateView):
    model=Breed
    fields="__all__"
    success_url=reverse_lazy('cats:index')

class UpdateBreed(LoginRequiredMixin, UpdateView):
    model=Breed
    fields='__all__'
    success_url=reverse_lazy('cats:index')

class DeleteBreed(LoginRequiredMixin, DeleteView):
    model=Breed
    fields='__all__'
    success_url=reverse_lazy('cats:index')






