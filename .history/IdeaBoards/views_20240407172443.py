from django.shortcuts import render

# Create your views here.
def IdeaBoards_Home(request):
    if request.user.is_authenticated:
        return render(request, 'ideaboard.html')
    else:
        return redirect('')