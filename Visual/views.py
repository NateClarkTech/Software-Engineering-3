from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from Visual.models import *

from django.shortcuts import render, redirect, get_object_or_404

#Bilge
@login_required
def visual(request):
    if request.method == "POST":
        if "visualNoteSubmit" in request.POST:
            title = request.POST.get('title', '').strip() # get the note title
            description = request.POST.get('description', '').strip() 
            image = request.POST.get('image', '').strip()
            if title or description or image: 
                VisualNote.objects.create(note_title=title, note_description=description, note_image=image)
        return redirect('visual')
    else: # if the method is GET
        notes = noteQuery()
        labels = labelQuery()
        return render(request, 'visual.html', {"notes":notes, "labels":labels})

def noteQuery():
    return VisualNote.objects.all().order_by('-created_at')
def labelQuery():
    return VisualLabel.objects.all().order_by("label_name")
