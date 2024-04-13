from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from Sound.models import *

from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.

#Bilge
@login_required
def sound(request):
    if request.method == "POST":
        if "soundNoteSubmit" in request.POST:
            title = request.POST.get('title', '').strip() # get the note title
            description = request.POST.get('description', '').strip()
            if title or description:  
                SoundNote.objects.create(note_title=title, note_description=description)
        return redirect('sound')
    else:
        notes = noteQuery()
        labels = labelQuery()
        return render(request, 'sound.html', {"notes":notes, "labels":labels})


def noteQuery():
    return SoundNote.objects.all().order_by('-created_at')
def labelQuery():
    return SoundLabel.objects.all().order_by("label_name")