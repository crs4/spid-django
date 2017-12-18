from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


@login_required
def protected_view(request):
    return HttpResponse("You logged in correctly")