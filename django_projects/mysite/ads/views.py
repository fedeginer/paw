from django.shortcuts import render, redirect, get_object_or_404
from ads.owner import OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .models import Ad, Comment, Fav
from django.db.models import Q
from .forms import CreateAd, CommentForm
from django.urls import reverse_lazy
from django.contrib.humanize.templatetags.humanize import naturaltime

class AdListView(OwnerListView):
    model=Ad
    template='ads/ad_list.html'
    # remodelamos el get
    def get(self, request):
        favor=list()
        strval =  request.GET.get("search", False)
        # hay que añadir este if porque la clase extendida OwnerListView no requiere de autentificacion
        if request.user.is_authenticated:
            rows=request.user.favorite_ads.values('id')
            favor=[ row.id for row in rows ]
        if strval :
            # Simple title-only search
            # objects = Post.objects.filter(title__contains=strval).select_related().order_by('-updated_at')[:10]

            # Multi-field search
            # __icontains for case-insensitive search
            query = Q(title__icontains=strval)
            query.add(Q(text__icontains=strval), Q.OR)
            objects = Ad.objects.filter(query).select_related().order_by('-updated_at')[:10]
        else :
            # try both versions with > 4 posts and watch the queries that happen
            objects = Ad.objects.all().order_by('-updated_at')[:10]
            # objects = Post.objects.select_related().all().order_by('-updated_at')[:10]

        # Augment the post_list
        for obj in objects:
            obj.natural_updated = naturaltime(obj.updated_at)
        return render(request, self.template, {'ad_list':objects, 'favorites':favor, 'search': strval})

class AdDetailView(OwnerDetailView):
    template='ads/ad_detail.html'
    success_url=reverse_lazy('ads:all')
    def get(self, request, pk):
        ad=Ad.objects.get(id=pk)
        form=CommentForm()
        comments=Comment.objects.filter(ad=ad).order_by('updated_at')
        return render(request, self.template, {'form':form, 'comments':comments, 'ad':ad})

class AdCreateView(LoginRequiredMixin, View):
    template_name = 'ads/ad_form.html'
    success_url = reverse_lazy('ads:all')

    def get(self, request, pk=None):
        form = CreateAd()
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        # el or None lo que quiere decir es que no es obligatorio que incluya una foto
        form = CreateAd(request.POST, request.FILES or None)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        # Add owner to the model before saving
        pic = form.save(commit=False)
        pic.owner = self.request.user
        pic.save()
        return redirect(self.success_url)

class CreateComment(LoginRequiredMixin, View):
    def post(self, request, pk):
        ad=get_object_or_404(Ad, id=pk)
        com=Comment(text=request.POST["comment"], ad=ad, owner=request.user)
        com.save()
        return redirect(reverse_lazy('ads:ad_detail', args=[pk]))

class DeleteComment(OwnerDeleteView):
    model=Comment
    template='ads/comment_confirm_delete.html'

    def get_success_url(self):
        ad=self.model.objects.ad
        return redirect(reverse_lazy('ads:ad_detail', args=[ad.id]))

class AdUpdateView(LoginRequiredMixin, View):
    template_name = 'ads/ad_form.html'
    success_url = reverse_lazy('pics:all')

    def get(self, request, pk):
        ad = get_object_or_404(Ad, id=pk, owner=self.request.user)
        form = CreateAd(instance=ad)
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        ad = get_object_or_404(Ad, id=pk, owner=self.request.user)
        form = CreateAd(request.POST, request.FILES or None, instance=ad)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        ad = form.save(commit=False)
        ad.save()

        return redirect(self.success_url)

class AdDeleteView(OwnerDeleteView):
    model=Ad
    fields=["title","price","text"]

def Picture(request, pk):
    # cogemos el objecto
    pic=get_object_or_404(Ad, id=pk)
    # creamos un objeto response
    response=HttpResponse()
    # añadimos los encabezados del response
    response['Content-type']=pic.content_type
    response['Content-Length']=len(pic.picture)
    # añadimos el response propiamente dicho
    response.write(pic.picture)
    return response

# csrf exemption in class based views
# https://stackoverflow.com/questions/16458166/how-to-disable-djangos-csrf-validation
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.utils import IntegrityError

@method_decorator(csrf_exempt, name='dispatch')
class AddFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        print("Add PK",pk)
        t = get_object_or_404(Ad, id=pk)
        fav = Fav(user=request.user, ad=t)
        try:
            fav.save()  # In case of duplicate key
        except IntegrityError as e:
            pass
        return HttpResponse()

@method_decorator(csrf_exempt, name='dispatch')
class DeleteFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        print("Delete PK",pk)
        t = get_object_or_404(Ad, id=pk)
        try:
            fav = Fav.objects.get(user=request.user, ad=t).delete()
        except Fav.DoesNotExist as e:
            pass

        return HttpResponse()
