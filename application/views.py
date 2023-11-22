from django.shortcuts import render
from django.shortcuts import redirect

# Create your views here.
def handle_not_found(request):
    return redirect('/custom-not-found-page/')