from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth.decorators import login_required

# Create your views here.
def IdeaBoards_Home(request):
    #If the user is logged in render the boards page
    if request.user.is_authenticated:
        boards = IdeaBoard.objects.filter(user=request.user)

        return render(request, 'ideaboard.html', {'boards': boards})
    #If the user is not logged in redirect to landing page
    else:
        return redirect('/')
    
def IdeaBoards_Create(request):
    #If the user is logged in render the create board page
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = NewIdeaBoardForm(request.POST)
            if form.is_valid():
                new_board = form.save(commit=False)
                new_board.user = request.user
                new_board.save()
                return redirect('IdeaBoards_Home')
        else:
            form = NewIdeaBoardForm(instance=request.user)

        return render(request, 'newboard.html', {'form': form})
    #If the user is not logged in redirect to landing page
    else:
        return redirect('/')
    
@login_required
def IdeaBoard_Detail(request, id):
    board = IdeaBoard.objects.get(id=id)
    items = IdeaBoardItem.objects.filter(instance=request.user, ideaboard=board)
    form = NewIdeaBoardItemForm(request.POST)
    return render(request, 'boarddetail.html', {'board': board, 'items': items, 'form': form})