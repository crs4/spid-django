from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render


@login_required
def protected_view(request):
    return HttpResponse("You logged in correctly")


def home(request):
    return render(request, 'index.html')