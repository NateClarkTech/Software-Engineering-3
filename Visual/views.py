from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout


from django.shortcuts import render, redirect, get_object_or_404

#Bilge


@login_required
def visual(request):
    return render(request, "visual.html")