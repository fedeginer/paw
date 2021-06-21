from django.urls import path
from . import views

app_name='cats'

urlpatterns=[
    path('', views.CatsIndex.as_view(), name='index'),
    path('updatecat/<int:pk>', views.UpdateCat.as_view(), name='updatecat'),
    path('deletecat/<int:pk>',views.DeleteCat.as_view(), name='deletecat'),
    path('addcat', views.CreateCat.as_view(),name='addcat'),
    path('breedlist', views.BreedList.as_view(), name='breedlist'),
    path('addbreed', views.CreateBreed.as_view(), name='addbreed'),
    path('updatebreed/<int:pk>', views.UpdateBreed.as_view(), name='updatebreed'),
    path('deletebreed/<int:pk>', views.DeleteBreed.as_view(), name='deletebreed'),
    ]