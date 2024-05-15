from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.contrib.auth.decorators import login_required
import json
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponseForbidden
from IdeaBoards.spotify import *
from django.http import JsonResponse
from django.core.files.uploadedfile import TemporaryUploadedFile

"""
    views.py

    Handles the views for the IdeaBoards app
    /boards/ - IdeaBoards_Home
    /boards/<int:id> - IdeaBoard_Detail

    Author:
        Nathaniel Clark
    """

def IdeaBoards_Home(request):
    """
    IdeaBoards_Home view

    Shows the user all their boards and allows them to create new boards

    Parameters:
        request (session): The details of the user's request for the page

    Returns:
        render: The HTML for the boards page

    Author:
        Nathaniel Clark
    """
    #If the user is logged in render the boards page
    if request.user.is_authenticated:
        print(request.POST, request.method)
        print(request.body.decode('utf-8'))

        #If the request is a POST request
        if request.method == 'POST':
            #Check to make sure the new board is a valid input
            form = NewIdeaBoardForm(request.POST)
            if form.is_valid():
                new_board = form.save(commit=False)
                new_board.user = request.user
                new_board.save()
                return redirect('IdeaBoards_Home')


        # @Bilge_AKYOL
        if request.method == "GETRECC":
            genre_name = json.loads(request.body.decode('utf-8'))[0]["genreName"] #parsing the javascript data

            #if the genre name is not null get the recommendations
            if genre_name:
                data = get_recc(genre_name) #calling the function from spotify.py
                response_data = {'message': data}
                return JsonResponse(response_data) #returning the output to javascript
        
        #Get the new board form and boards for the user
        form = NewIdeaBoardForm(instance=request.user)
        boards = IdeaBoard.objects.filter(user=request.user)
        
        # Retrieve error message from session if it exists 
        error_message = request.session.pop('error_messages', None)
        #print (error_message)

        #Render the boards page
        return render(request, 'ideaboard.html', {'boards': boards, 'form': form, 'error_message': error_message})
    #If the user is not logged in redirect to landing page
    else:
        # User is not logged in, redirect to landing page
        return redirect('home')
    

@login_required
def IdeaBoard_Detail(request, id):
    """
    IdeaBoard_Detail view

    Shows the user a specific board and allows them to edit the board and its items if the user is the owner of the board
    Otherwise, the user can only view the board if the board is public
    Also allows the user to add, edit, and delete items on the board
    Edit and delete the board

    Parameters:
        request (session): The details of the user's request for the page
        id (int): The ID of the board to be displayed

    Returns:
        render: The HTML for the current board

    Author:
        Nathaniel Clark
    """
    #make sure the board exists, if not redirect to the boards page
    try:
        board = IdeaBoard.objects.get(id=id)
        items = IdeaBoardItem.objects.filter(ideaboard=board)
        labels = ItemLabel.objects.filter(label_board=board) #filtering labels by the board so that the labels are unique to the board

    #If the board does not exist redirect to the boards page
    except:
        # error implementation was based on GPT https://chat.openai.com/share/424d6891-b553-4829-b8fd-8eafd56f687c
        error_messages = request.session.get('error_messages', [])
        # Append the new error message
        error_messages.append(str(id) + " is not a valid board ID.")
        # Store the updated error messages list back into the session
        request.session['error_messages'] = error_messages
        return redirect('IdeaBoards_Home')

    #If the user is the owner of the board
    if board.user == request.user:

        """**************************************************************************************
        *  POST REQUEST:  Go through changes to the board and make the changes to the database  *
        **************************************************************************************"""
        # @Bilge_AKYOL
        if request.method == "GETRECC":
            genre_name = json.loads(request.body.decode('utf-8'))[0]["genreName"] #parsing the javascript data
            if genre_name:
                data = get_recc(genre_name) #calling the function from spotify.py
                response_data = {'message': data}
                return JsonResponse(response_data) #returning the output to javascript
            
            
        if request.method == 'POST':
           handle_database_changes(request, board)

            
        """************************************
        *  DELETE REQUEST:  Delete the board  *
        ************************************"""
        if request.method == 'DELETE':

            #redirects to IdeaBoards_Home after deleting the board
            return handle_delete_request(request, board) 
        
        #give the HTML for the board with the board's items
        return render(request, 'boarddetail.html', {'board': board, 'items': items, 'labels': labels})
    
    #If the board is public give the user the HTML for the board
    elif board.is_public:
        comments = BoardComment.objects.all()
        return render(request, 'publicboarddetails.html', {'board': board, 'items': items, 'labels': labels, 'board_comments': comments})
    
    #If the user is not the owner of the board redirect to them to their boards
    else:
        # error implementation was based on GPT https://chat.openai.com/share/424d6891-b553-4829-b8fd-8eafd56f687c
        error_messages = request.session.get('error_messages', [])
        # Append the new error message
        error_messages.append("You do not have permission to view this board.")
        # Store the updated error messages list back into the session
        request.session['error_messages'] = error_messages
        return redirect('IdeaBoards_Home')

#@W_Farmer, adapted by Bilge_AKYOL
# This view will allow the user to create a new comment on the forum. 
@login_required
def create_comment(request, id, comment_id=None):
    board = get_object_or_404(IdeaBoard, id=id)
    form = CommentForm(request.POST)
    
    if form.is_valid():
        comment_content = form.cleaned_data['content']
        # Convert YouTube links to embeds

        # Convert links to embeds and sanitize
        #comment_content = convert_media_links_to_embed(comment_content)
        #comment_content = clean_html(comment_content)  # Clean the HTML

        # Create the comment object
        comment = form.save(commit=False)
        comment.content = comment_content  # Set the processed content with YouTube embeds
        # Associate the comment with the thread and the logged-in user
        comment.user = request.user
        comment.board = board
        comment.save()

        # Remove the comment author to prevent them from receiving their own notification
        #recipients.discard(request.user)

        # Create notifications for each unique recipient
        '''
        for recipient in recipients:
            Notification.objects.create(
                notification_type=Notification.COMMENT,
                to_user=recipient,
                from_user=request.user,
                thread=thread,
                comment=comment
            )
        '''
        return redirect(reverse('IdeaBoard_Detail', args=[board.id]))
    else:
        # Handle errors or redirect
        return redirect('IdeaBoard_Detail', board.id)

#@W_Farmer, adapted by @Bilge_AKYOL
# This is a view to allow the user to delete a comment, they have to be the author of the comment, or a superuser
def delete_comment(request, comment_id):
    # Add a check to see uf the user is authentacated at all
    if not request.user.is_authenticated:
        return HttpResponseForbidden("You are not authorized to delete this comment.")
    
    comment = get_object_or_404(BoardComment, id=comment_id)
    
    # Check if the user is the author of the comment or a superuser
    if request.user != comment.user and not request.user.is_superuser:
        # Throw an error, they are not authorized to do this
        return HttpResponseForbidden("You are not authorized to delete this comment.")
    comment.delete()
    return redirect('IdeaBoard_Detail', id=comment.board.id)

#@W_Farmer, adapted by @Bilge_AKYOL
# Here we want to be able to edit a comment, either by deleating it, or by changing the content, and the user HAS to be the one logged in, or a superuser
@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(BoardComment, id=comment_id)
    # Check if the user is the author of the comment or a superuser
    if request.user != comment.user and not request.user.is_superuser:
        # Throw an error, they are not authorized to do this
        return HttpResponseForbidden("You are not authorized to edit this comment.")
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('IdeaBoard_Detail', id=comment.board.id)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'edit_board_comment.html', {'form': form, 'comment': comment})

#@W_Farmer, adapted by @Bilge_AKYOL
# This is a view that will allow a user to like a comment, or unlike said comment
def like_comment(request, comment_id):
    # Some checks to make sure that the user cannot like their comment, even by messing with the urls

    comment = get_object_or_404(BoardComment, id=comment_id)
    if request.user == comment.user and not request.user.is_superuser:
        # Throw an error, they are not authorized to do this
        return HttpResponseForbidden("You shouldn't be seeing this. bad. no liking this comment.")
    if request.user in comment.likes.all():
        comment.likes.remove(request.user)
    else:
        comment.likes.add(request.user)
    return redirect('IdeaBoard_Detail', id=comment.board.id)

def handle_database_changes(request, board):
    """
    handle_database_changes view

    Handles the changes to the database for the board

    Parameters:
        request (session): The details of the user's request for the page

    Warning:
        This function should not be used as a view

    Returns:
        redirect: Redirects the user to the boards page

    Author:
        Nathaniel Clark
    """
     # Get form data
    form_data = request.POST
    # Get file data
    file_data = request.FILES

    print(form_data)
    print(file_data)

    number_of_changes = form_data.get('numChanges')
    #print(number_of_changes)

    # Loop through the number of changes
    for index in range(int(number_of_changes)):
        #print("iteration:", x)
        change_type = form_data.get(f'{index}_change_type')
        #print(change_type)
            
        # If the operation is to add a new item
        if change_type == 'add':
            add_item_to_board(request, form_data, file_data, board, index)

        # If the operation is to edit an existing item
        elif change_type == 'edit':
            edit_item_on_board(request, form_data, file_data, board, index)

        # If the operation is to delete an existing item
        elif change_type == 'delete':
            delete_item_on_board(request, form_data, board, index)  

        # If the operation is to edit the details of the board
        elif change_type == 'editBoardDetails':
            edit_board_details(request, form_data, board, index)

        # If the operation is to add a new label
        elif change_type == 'addLabel':
            add_label_to_database(request, form_data, board, index)

        # Something very very wrong happened
        else:
            print('not a valid change type')
            print ("Change Type:", change_type)

def handle_delete_request(request, board):
    """
    handle_delete_request for IdeaBoard_Detail view

    Handles the delete request for the board

    Parameters:
        request (session): The details of the user's request for the page

    Warning:
        This function should not be used as a view
        
    Returns:
        redirect: Redirects the user to the boards page

    Author:
        Nathaniel Clark
    """
    # Get the data from the request
    data = json.loads(request.body.decode('utf-8'))
    data = data[0]
    board = IdeaBoard.objects.get(id=data['board_id'])
    
    #print(board.user, request.user, data)

    board.delete()

    #print('deleted')
    return redirect('IdeaBoards_Home')

def add_item_to_board(request, form_data, file_data, board, index):
    """
    add_item_to_board view

    Adds an item to the board

    Parameters:
        request (session): The details of the user's request for the page

    Warning:
        This function should not be used as a view

    Returns:
        redirect: Redirects the user to the boards page

    Author:
        Nathaniel Clark
    """
    item_label = form_data.get(f'{index}_item_label')
    if item_label == 'null':
        label = None
    else:
        label = ItemLabel.objects.get(label_name=item_label, label_board=board)

    

    item_image_files = file_data.getlist(f'{index}_item_image')

    # Check if there are any uploaded files for '0_item_image'
    if item_image_files:
        item_image_file = item_image_files[0]
        
        # Create a TemporaryUploadedFile instance
        temporary_uploaded_image = TemporaryUploadedFile(
            name=item_image_file.name,  # Set the name of the file
            content_type=item_image_file.content_type,  # Set the content type of the file
            size=item_image_file.size,  # Set the size of the file
            charset=None  # Charset is not applicable for binary files
        )

        # Write the file content to the TemporaryUploadedFile
        temporary_uploaded_image.write(item_image_file.read())

        # Move the file pointer back to the beginning of the file
        temporary_uploaded_image.seek(0)

    item_sound_files = file_data.getlist(f'{index}_item_sound')

    # Check if there are any uploaded files for '0_item_sound'
    if item_sound_files:
        item_sound_file = item_sound_files[0]
        
        # Create a TemporaryUploadedFile instance for audio
        temporary_uploaded_audio = TemporaryUploadedFile(
            name=item_sound_file.name,  # Set the name of the file
            content_type=item_sound_file.content_type,  # Set the content type of the file
            size=item_sound_file.size,  # Set the size of the file
            charset=None  # Charset is not applicable for binary files
        )

        # Write the file content to the TemporaryUploadedFile
        temporary_uploaded_audio.write(item_sound_file.read())

        # Move the file pointer back to the beginning of the file
        temporary_uploaded_audio.seek(0)


    # Create a dictionary of form data
    formData = {
        "title": form_data.get(f'{index}_title'),
        "description": form_data.get(f'{index}_description'),
        "note_label": label,
    }
    # Create a dictionary of file data
    fileData = {
        "item_image": temporary_uploaded_image if item_image_files else None,
        "item_sound": temporary_uploaded_audio if item_sound_files else None,
    }

    form = NewIdeaBoardItemForm(formData, fileData) # Pass both form data and file data # type: ignore 

    # Check if the form is valid save the item
    if form.is_valid():
        new_item = form.save(commit=False)
        new_item.owner = request.user
        new_item.ideaboard = board
        new_item.save()
    else:
        print(form.errors)

def edit_item_on_board(request, form_data, file_data, board, index):
    """
    edit_item_on_board view

    Edits an item on the board

    Parameters:
        request (session): The details of the user's request for the page

    Warning:
        This function should not be used as a view

    Returns:
        redirect: Redirects the user to the boards page

    Author:
        Nathaniel Clark
    """
    # Get the item to be edited from the database
    editedItem = IdeaBoardItem.objects.get(id=form_data.get(f'{index}_item_id'))
    editedItem.title = form_data.get(f'{index}_title')
    editedItem.description = form_data.get(f'{index}_description')
    
    remove_label = form_data.get(f'{index}_remove_label')
    if (remove_label == "true"):
        editedItem.note_label = None
    elif form_data.get(f'{index}_item_label'):
        editedItem.note_label = ItemLabel.objects.get(label_name=form_data.get(f'{index}_item_label'), label_board=board)

    # Check if the user has uploaded a new image for the item
    item_image_files = file_data.getlist(f'{index}_item_image')
    # Check if there are any uploaded files for '0_item_image'
    if item_image_files:
        item_image_file = item_image_files[0]
        
        # Create a TemporaryUploadedFile instance
        temporary_uploaded_image = TemporaryUploadedFile(
            name=item_image_file.name,  # Set the name of the file
            content_type=item_image_file.content_type,  # Set the content type of the file
            size=item_image_file.size,  # Set the size of the file
            charset=None  # Charset is not applicable for binary files
        )

        # Write the file content to the TemporaryUploadedFile
        temporary_uploaded_image.write(item_image_file.read())

        # Move the file pointer back to the beginning of the file
        temporary_uploaded_image.seek(0)
        editedItem.item_image = temporary_uploaded_image # type: ignore

    # Check if the user has uploaded a new audio file for the item
    item_sound_files = file_data.getlist(f'{index}_item_sound')

    # Check if there are any uploaded files for '0_item_sound'
    if item_sound_files:
        item_sound_file = item_sound_files[0]
        
        # Create a TemporaryUploadedFile instance for audio
        temporary_uploaded_audio = TemporaryUploadedFile(
            name=item_sound_file.name,  # Set the name of the file
            content_type=item_sound_file.content_type,  # Set the content type of the file
            size=item_sound_file.size,  # Set the size of the file
            charset=None  # Charset is not applicable for binary files
        )

        # Write the file content to the TemporaryUploadedFile
        temporary_uploaded_audio.write(item_sound_file.read())

        # Move the file pointer back to the beginning of the file
        temporary_uploaded_audio.seek(0)
        editedItem.item_sound = temporary_uploaded_audio # type: ignore


    # If the user removed image or sound remove them from the item
    remove_image = form_data.get(f'{index}_remove_image')
    if (remove_image == "true"):
        editedItem.item_image = None # type: ignore

    remove_audio = form_data.get(f'{index}_remove_sound')
    if (remove_audio == "true"):
        editedItem.item_sound = None # type: ignore



    # Save the edited item
    editedItem.save()

def delete_item_on_board(request, form_data, board, index):
    """
    delete_item_on_board view

    Deletes an item on the board

    Parameters:
        request (session): The details of the user's request for the page

    Warning:
        This function should not be used as a view

    Returns:
        redirect: Redirects the user to the boards page

    Author:
        Nathaniel Clark
    """
    item = IdeaBoardItem.objects.get(id=form_data.get(f'{index}_item_id'))
    item.delete()

def edit_board_details(request, form_data, board, index):
    """
    edit_board_details view

    Edits the details of the board

    Parameters:
        request (session): The details of the user's request for the page

    Warning:
        This function should not be used as a view

    Returns:
        redirect: Redirects the user to the boards page

    Author:
        Nathaniel Clark
    """
    # Update the board details
    board.title = form_data.get(f'{index}_title')
    board.description = form_data.get(f'{index}_description')

    # Set the privacy setting of the board
    if form_data.get(f'{index}_privacy_setting') == 'true':
        board.is_public = True
    else:
        board.is_public = False

    # Save the board
    board.save()

def add_label_to_database(request, form_data, board, index):
    """
    add_label_to_database view

    Adds a label to the database

    Parameters:
        request (session): The details of the user's request for the page

    Warning:
        This function should not be used as a view

    Returns:
        None

    Author:
        Bilge Akyol
    """
    # Create a dictionary of form data
    formData = {
        "label_name": form_data.get(f'{index}_labelName'),
    }
    #print(formData)
    
    # Create a new label
    form = NewItemLabelForm(formData)
    # Check if the form is valid save the label
    if form.is_valid():
        new_label = form.save(commit=False)
        new_label.label_board = board
        new_label.save()
    else:
        print(form.errors)