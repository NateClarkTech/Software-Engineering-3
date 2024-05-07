from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth.decorators import login_required
import json
from django.urls import reverse
from django.http import HttpResponseRedirect
from IdeaBoards.spotify import *
from django.http import JsonResponse
from django.core.files.uploadedfile import TemporaryUploadedFile

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
def IdeaBoard_Detail(request, id):
    #make sure the board exists, if not redirect to the boards page
    try:
        board = IdeaBoard.objects.get(id=id)
        items = IdeaBoardItem.objects.filter(ideaboard=board)

    except:
        # error implementation was based on GPT https://chat.openai.com/share/424d6891-b553-4829-b8fd-8eafd56f687c
        error_messages = request.session.get('error_messages', [])
        # Append the new error message
        error_messages.append(str(id) + " is not a valid board ID.")
        # Store the updated error messages list back into the session
        request.session['error_messages'] = error_messages
        return redirect('IdeaBoards_Home')
        
    #print(request.method)

    #If the user is the owner of the board
    if board.user == request.user:
        if request.method == 'POST':
            # Get form data
            form_data = request.POST
            # Get file data
            file_data = request.FILES

            #print(form_data)
            #print(file_data)

            number_of_changes = form_data.get('numChanges')
            #print(number_of_changes)

            for x in range(int(number_of_changes)):
                #print("iteration:", x)
                change_type = form_data.get(f'{x}_change_type')
                #print(change_type)

                if change_type == 'add':
                    formData = {
                        "title": form_data.get(f'{x}_title'),
                        "description": form_data.get(f'{x}_description'),
                    }

                    board_image_files = file_data.getlist(f'{x}_board_image')

                    # Check if there are any uploaded files for '0_board_image'
                    if board_image_files:
                        board_image_file = board_image_files[0]
                        
                        # Create a TemporaryUploadedFile instance
                        temporary_uploaded_image = TemporaryUploadedFile(
                            name=board_image_file.name,  # Set the name of the file
                            content_type=board_image_file.content_type,  # Set the content type of the file
                            size=board_image_file.size,  # Set the size of the file
                            charset=None  # Charset is not applicable for binary files
                        )

                        # Write the file content to the TemporaryUploadedFile
                        temporary_uploaded_image.write(board_image_file.read())

                        # Move the file pointer back to the beginning of the file
                        temporary_uploaded_image.seek(0)

                    board_sound_files = file_data.getlist(f'{x}_board_sound')

                    # Check if there are any uploaded files for '0_board_sound'
                    if board_sound_files:
                        board_sound_file = board_sound_files[0]
                        
                        # Create a TemporaryUploadedFile instance for audio
                        temporary_uploaded_audio = TemporaryUploadedFile(
                            name=board_sound_file.name,  # Set the name of the file
                            content_type=board_sound_file.content_type,  # Set the content type of the file
                            size=board_sound_file.size,  # Set the size of the file
                            charset=None  # Charset is not applicable for binary files
                        )

                        # Write the file content to the TemporaryUploadedFile
                        temporary_uploaded_audio.write(board_sound_file.read())

                        # Move the file pointer back to the beginning of the file
                        temporary_uploaded_audio.seek(0)

                    fileData = {
                        "board_image": temporary_uploaded_image if board_image_files else None,
                        "board_sound": temporary_uploaded_audio if board_sound_files else None,
                    }

                    form = NewIdeaBoardItemForm(formData, fileData)  # Pass both form data and file data

                    if form.is_valid():
                        new_item = form.save(commit=False)
                        new_item.owner = request.user
                        new_item.ideaboard = board
                        new_item.save()
                    else:
                        print(form.errors)


                elif change_type == 'edit':
                    editedItem = IdeaBoardItem.objects.get(id=form_data.get(f'{x}_item_id'))
                    editedItem.title = form_data.get(f'{x}_title')
                    editedItem.description = form_data.get(f'{x}_description')
                    editedItem.save()

                elif change_type == 'delete':
                    item = IdeaBoardItem.objects.get(id=form_data.get(f'{x}_item_id'))
                    item.delete()

                elif change_type == 'editBoardDetails':
                    board.title = form_data.get(f'{x}_title')
                    board.description = form_data.get(f'{x}_description')
                    if form_data.get(f'{x}_privacy_setting') == 'true':
                        board.is_public = True
                    else:
                        board.is_public = False
                    board.save()
                
                else:
                    print('not a valid change type')
            
        if request.method == 'DELETE':
            data = json.loads(request.body.decode('utf-8'))
            data = data[0]
            board = IdeaBoard.objects.get(id=data['board_id'])
            print("this is printing")
            print(board.user, request.user, data)
            if board.user == request.user:
                board.delete()

                print('deleted')
                return redirect('IdeaBoards_Home')

        
        #give the HTML for the board with the board's items
        return render(request, 'boarddetail.html', {'board': board, 'items': items})
    
    elif board.is_public:
        return render(request, 'publicboarddetails.html', {'board': board, 'items': items})
    
    #If the user is not the owner of the board redirect to them to their boards
    else:
        # error implementation was based on GPT https://chat.openai.com/share/424d6891-b553-4829-b8fd-8eafd56f687c
        error_messages = request.session.get('error_messages', [])
        # Append the new error message
        error_messages.append("You do not have permission to view this board.")
        # Store the updated error messages list back into the session
        request.session['error_messages'] = error_messages
        return redirect('IdeaBoards_Home')
