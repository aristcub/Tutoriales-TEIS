from django.shortcuts import render
from django.http import HttpResponse # new

def homePageView(request): # new
 return HttpResponse('Hello World!') # new
# Create your views here.
