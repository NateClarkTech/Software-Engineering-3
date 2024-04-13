from django.shortcuts import render

# Create your views here.
def IdeaBoards_Home(request):
    return render(request, 'IdeaBoards/ideaboard.html')