from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth.decorators import login_required
import json
from django.urls import reverse
from django.http import HttpResponseRedirect
from IdeaBoards.spotify import *
from django.http import JsonResponse

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
        print(request.body.decode('utf-8'))

        #If the request is a POST request
        if request.method == 'POST':
            form = NewIdeaBoardForm(request.POST)
            if form.is_valid():
                new_board = form.save(commit=False)
                new_board.user = request.user
                new_board.save()
                return redirect('IdeaBoards_Home')

        if request.method == "GETRECC":
            genre_name = json.loads(request.body.decode('utf-8'))[0]["genreName"]
            if genre_name:
                data = get_recc(genre_name)
                response_data = {'message': data}
                return JsonResponse(response_data)
        
        form = NewIdeaBoardForm(instance=request.user)
        boards = IdeaBoard.objects.filter(user=request.user)
         # Retrieve error message from session if it exists
        error_message = request.session.pop('error_messages', None)

        print (error_message)

        return render(request, 'ideaboard.html', {'boards': boards, 'form': form, 'error_message': error_message})
    #If the user is not logged in redirect to landing page
    else:
        return redirect('home')
    

"""
IdeaBoard_Details: 
    This is a view for a board
    This page will display all the notes on the board
    Users can add, delete, and edit notes on the board
"""
@login_required
def IdeaBoard_Detail(request, id, label=None):
    #make sure the board exists, if not redirect to the boards page
    try:
        board = IdeaBoard.objects.get(id=id)
    except:
        # error implementation was based on GPT https://chat.openai.com/share/424d6891-b553-4829-b8fd-8eafd56f687c
        error_messages = request.session.get('error_messages', [])
        # Append the new error message
        error_messages.append(str(id) + " is not a valid board ID.")
        # Store the updated error messages list back into the session
        request.session['error_messages'] = error_messages
        return redirect('IdeaBoards_Home')
    
    labels = ItemLabel.objects.filter(label_board=board)
    if(label==None):
        items = IdeaBoardItem.objects.filter(ideaboard=board)
    else:
        label_id = labels.get(label_name=label)
        items = IdeaBoardItem.objects.filter(ideaboard=board, note_label=label_id)
        
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
                elif item['changeType'] == 'edit':
                    editedIitem = IdeaBoardItem.objects.get(id=item['item_id'])
                    editedIitem.title = item['title']
                    editedIitem.description = item['description']
                    editedIitem.save()

                #if the changeType is delete, delete the item from the database
                elif item['changeType'] == 'delete':
                    item = IdeaBoardItem.objects.get(id=item['item_id']).delete()

                #if the changeType is editBoardDetails, edit the board title and description
                elif item['changeType'] == 'editBoardDetails':
                    board.title = item['title']
                    board.description = item['description']
                    board.save()
            
        if request.method == 'DELETE':
            data = json.loads(request.body.decode('utf-8'))
            data = data[0]
            board = IdeaBoard.objects.get(id=data['board_id'])
            if board.user == request.user:
                board.delete()

                print('deleted')
                return redirect('IdeaBoards_Home')

    
        #give the HTML for the board with the board's items
        return render(request, 'boarddetail.html', {'board': board, 'items': items, "labels": labels})
    
    #If the user is not the owner of the board redirect to them to their boards
    else:
        # error implementation was based on GPT https://chat.openai.com/share/424d6891-b553-4829-b8fd-8eafd56f687c
        error_messages = request.session.get('error_messages', [])
        # Append the new error message
        error_messages.append("You do not have permission to view this board.")
        # Store the updated error messages list back into the session
        request.session['error_messages'] = error_messages
        return redirect('IdeaBoards_Home')