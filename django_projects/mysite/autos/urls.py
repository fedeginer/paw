from django.urls import path
from . import views

app_name='autos'
urlpatterns=[
    path('',views.Autos_list.as_view(), name='autos_list'),
    path('lookup', views.Makes_list.as_view(), name='listmakes'),
    path('lookup/create', views.Add_make.as_view(), name='addmakes'),
    path('main/create',views.Add_auto.as_view(), name='addauto'),
    path('lookup/<int:id>/update', views.Update_make.as_view(), name='updatemakes'),
    path('main/<int:id>/update', views.Update_auto.as_view(), name='updateautos'),
    path('main/<int:id>/delete', views.Delete_auto.as_view(), name='deleteauto'),
    path('lookup/<int:id>/delete', views.Delete_make.as_view(), name='deletemakes'),
]