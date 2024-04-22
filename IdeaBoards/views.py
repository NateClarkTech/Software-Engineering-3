from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth.decorators import login_required
import json

# Create your views here.
def IdeaBoards_Home(request):
    #If the user is logged in render the boards page
    if request.user.is_authenticated:

        if request.method == 'POST':
            print(request.POST, request.method)
            form = NewIdeaBoardForm(request.POST)
            if form.is_valid():
                new_board = form.save(commit=False)
                new_board.user = request.user
                new_board.save()
        
        form = NewIdeaBoardForm(instance=request.user)
        boards = IdeaBoard.objects.filter(user=request.user)
        return render(request, 'ideaboard.html', {'boards': boards, 'form': form})
    #If the user is not logged in redirect to landing page
    else:
        return redirect('/')
    
@login_required
def IdeaBoard_Detail(request, id):
    board = IdeaBoard.objects.get(id=id)
    items = IdeaBoardItem.objects.filter(ideaboard=board)

    #If the user is the owner of the board
    if request.user == board.user:

        #If the fetch request is a POST request, save the changes to the board to the database
        if request.method == 'POST':
            print(request.body, request.POST, request.method)

            #get the data from the body and decode it
            data = json.loads(request.body.decode('utf-8'))

            #for each item in the json update the database properly
            for item in data:
                #print(item)

                #if the type is add, add the item to the database pointing at the board
                if (item['type'] == 'add'):
                    form = NewIdeaBoardItemForm(item)
                    if form.is_valid():
                        new_item = form.save(commit=False)
                        new_item.owner = request.user
                        new_item.ideaboard = board
                        new_item.save()
    
        #give the HTML for the board with the board's items
        return render(request, 'boarddetail.html', {'board': board, 'items': items})
    
    #If the user is not the owner of the board redirect to them to their boards
    else:
        return render('IdeaBoards_Home')