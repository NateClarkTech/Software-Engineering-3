from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth.decorators import login_required
import json

"""
IdeaBoards_Home: 
    This is a view for the databoards.
    This page will display all the boards a user owns
    Users can create, delete, edit, and view their boards
"""
def IdeaBoards_Home(request):
    #If the user is logged in render the boards page
    if request.user.is_authenticated:

        print(request.POST, request.method)

        #If the request is a POST request
        if request.method == 'POST':
            form = NewIdeaBoardForm(request.POST)
            if form.is_valid():
                new_board = form.save(commit=False)
                new_board.user = request.user
                new_board.save()
                
        if request.method == 'PATCH':
            data = json.loads(request.body.decode('utf-8'))
            
            #update the board in the database
            for item in data:
                if item['type'] == 'edit':
                    print(item)
                    board = IdeaBoard.objects.get(id=item['board_id'])
                    board.title = item['newTitle']
                    board.description = item['newDescription']
                    board.save()


        #If the request is a DELETE request
        if request.method == 'DELETE':
            data = json.loads(request.body.decode('utf-8'))
            
            #Delete the board from the database
            for item in data:
                if item['type'] == 'delete':
                    board = IdeaBoard.objects.get(id=item['board_id']).delete()

        
        form = NewIdeaBoardForm(instance=request.user)
        boards = IdeaBoard.objects.filter(user=request.user)
        return render(request, 'ideaboard.html', {'boards': boards, 'form': form})
    #If the user is not logged in redirect to landing page
    else:
        return redirect('/')
    

"""
IdeaBoard_Details: 
    This is a view for a board
    This page will display all the notes on the board
    Users can add, delete, and edit notes on the board
"""
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

                #if the changeType is add, add the item to the database pointing at the board
                if (item['changeType'] == 'add'):
                    form = NewIdeaBoardItemForm(item)
                    if form.is_valid():
                        new_item = form.save(commit=False)
                        new_item.owner = request.user
                        new_item.ideaboard = board
                        new_item.save()

                #if the changeType is edit, edit the item in the database
                if item['changeType'] == 'edit':
                    editedIitem = IdeaBoardItem.objects.get(id=item['item_id'])
                    editedIitem.title = item['title']
                    editedIitem.description = item['description']
                    editedIitem.save()

                #if the changeType is delete, delete the item from the database
                if item['changeType'] == 'delete':
                    item = IdeaBoardItem.objects.get(id=item['item_id']).delete()
    
        #give the HTML for the board with the board's items
        return render(request, 'boarddetail.html', {'board': board, 'items': items})
    
    #If the user is not the owner of the board redirect to them to their boards
    else:
        return render('IdeaBoards_Home')