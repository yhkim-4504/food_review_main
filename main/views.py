from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def main_page(request):
    return render(request, 'main/main.html')

def menu_page(request):
    return render(request, 'main/menu.html')