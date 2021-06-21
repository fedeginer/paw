from django.shortcuts import render
from django.http import HttpResponse

def hello(request):
    num=request.session.get('num_view',0)+1
    request.session['num_view']=num
    response='8b2af218 view count='+str(num)
    response=HttpResponse(response)
    response.set_cookie('dj4e_cookie', '8b2af218', max_age=1000)
    return response
