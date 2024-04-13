from django.shortcuts import render, redirect
from .forms import *;

# Create your views here.
def IdeaBoards_Home(request):
    #If the user is logged in render the boards page
    if request.user.is_authenticated:
        return render(request, 'ideaboard.html')
    #If the user is not logged in redirect to landing page
    else:
        return redirect('/')
    
def IdeaBoards_Create(request):
    #If the user is logged in render the create board page
    if request.user.is_authenticated:
        form = 

        return render(request, 'newboard.html')
    #If the user is not logged in redirect to landing page
    else:
        return redirect('/')