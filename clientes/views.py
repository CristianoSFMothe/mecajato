from django.shortcuts import render
from django.http import HttpResponse

def clientes(request):
    return render(request, 'clientes.html')
