from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from Sound.models import *

from django.shortcuts import render, redirect, get_object_or_404
from Sound.spotify import *

# Bilge implemented this application.

@login_required
def sound(request):
    if request.method == "POST":
        if "soundNoteSubmit" in request.POST:
            title = request.POST.get('title', '').strip() # get the note title
            description = request.POST.get('description', '').strip()
            labelselect = request.POST.get("labelselect")
            label = get_object_or_404(SoundLabel, label_name=labelselect)
            if title or description or label:  
                SoundNote.objects.create(note_title=title, note_description=description, note_label=label)
        if "soundCreateLabel" in request.POST:
            label = request.POST.get('createLabel', "").strip()
            if label:
                SoundLabel.objects.create(label_name=label)
        if "get_recc" in request.POST:
            genre_name = request.POST.get('get_recc', '').strip()
            if genre_name:
                recc = get_recc(genre_name)
                notes = noteQuery()
                labels = labelQuery()
                return render(request, 'sound.html', {"notes":notes, "labels":labels, "recc":recc})
        return redirect('sound')
    else:
        notes = noteQuery()
        labels = labelQuery()
        return render(request, 'sound.html', {"notes":notes, "labels":labels})


def noteQuery():
    return SoundNote.objects.all().order_by('-created_at')
def labelQuery():
    return SoundLabel.objects.all().order_by("label_name")

@login_required
def label_sort(request, label_name):
    notes = noteQuery()
    labels = labelQuery()
    label = SoundLabel.objects.get(label_name=label_name)
    return render(request, 'label_sort.html', {'label': label, "notes":notes, "labels":labels})
