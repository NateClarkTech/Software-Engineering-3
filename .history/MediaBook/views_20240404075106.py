from django.shortcuts import render, redirect, get_object_or_404



def landingpage(request):
    return render(request, 'ncfhours.html')