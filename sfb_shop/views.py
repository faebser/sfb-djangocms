from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return HttpResponse("Hello test, you are at the index.")

def addToBasket(request):
    pass

def checkout(request):
    # check and send mail
    pass
