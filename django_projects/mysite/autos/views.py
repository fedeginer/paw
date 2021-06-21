from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Auto, Make
from .forms import AutoForm, MakeForm

class Autos_list(LoginRequiredMixin, View):
    template='autos/auto_list.html'
    def get(self,request):
        auto_list=Auto.objects.all()
        number_make=Make.objects.all().count()
        return render(request,self.template,{'autos':auto_list,'count':number_make})

class Makes_list(LoginRequiredMixin,View):
    template='autos/makes_list.html'
    def get(self,request):
        make_list=Make.objects.all()
        return render(request, self.template,{'makes_list':make_list})

class Add_make(LoginRequiredMixin, View):
    template='autos/make.html'
    success=reverse_lazy('autos:autos_list')
    def get(self,request):
        form=MakeForm()
        return render(request,self.template,{'form':form})
    def post(self,request):
        form=MakeForm(request.POST)
        if not form.is_valid():
            return render(request,self.template,{'form':form})
        else:
            # Make(name=name).save() esto no es necesario porque coinciden!!
            form.save()
            return redirect(self.success)

class Add_auto(LoginRequiredMixin,View):
    template='autos/auto.html'
    success=reverse_lazy('autos:autos_list')
    def get(self,request):
        form=AutoForm()
        return render(request, self.template,{'form':form})
    def post(self,request):
        form=AutoForm(request.POST)
        if not form.is_valid():
            render(request,self.template,{'form':form})
        else:
            #Auto(nickname=nickname,mileage=mileage,comments=comments,make=make).save() esto no es necesario porque coinciden!!
            form.save()
            return redirect(self.success)

class Update_make(LoginRequiredMixin,View):
    model=Make
    template='autos/make.html'
    success=reverse_lazy('autos:autos_list')
    def get(self,request, id):
        make=get_object_or_404(self.model,pk=id) # coge la instancia del model
        form=MakeForm(instance=make) # genera un formulario a partir de una instancia de un modelo
        return render(request,self.template,{'form':form})
    def post(self,request, id):
        make=get_object_or_404(self.model,pk=id)
        form=MakeForm(request.POST, instance=make) # rellena un formulario acompañado de un indicador de la instancia del modelo
        if not form.is_valid():
            return render(request,self.template,{'form':form})
        else:
            form.save() # rellena la instancia del modelo contenida en el form con el contenido del nuevo form
            return redirect(self.success)

class Update_auto(LoginRequiredMixin,View):
    model=Auto
    template='autos/auto.html'
    success=reverse_lazy('autos:autos_list')
    def get(self,request,id):
        auto=get_object_or_404(self.model,pk=id)
        form=AutoForm(instance=auto)
        return render(request,self.template,{'form':form})
    def post(self,request,id):
        auto=get_object_or_404(self.model,pk=id)
        form=AutoForm(request.POST, instance=auto)
        if not form.is_valid():
            return render(request, self.template,{'form':form})
        else:
            form.save()
            return redirect(self.success)

class Delete_auto(LoginRequiredMixin,View):
    model=Auto
    template='autos/eliminar.html'
    success=reverse_lazy('autos:autos_list')
    def get(self, request, id):
        auto=get_object_or_404(self.model, pk=id)
        return render(request,self.template,{'auto':auto})
    def post(self,request,id):
        auto=get_object_or_404(self.model, pk=id)
        auto.delete()
        return redirect(self.success)

class Delete_make(LoginRequiredMixin,View):
    model=Make
    template='autos/eliminar_make.html'
    success=reverse_lazy('autos:autos_list')
    def get(self, request, id):
        make=get_object_or_404(self.model, pk=id)
        return render(request,self.template,{'make':make})
    def post(self,request,id):
        make=get_object_or_404(self.model, pk=id)
        make.delete()
        return redirect(self.success)

