from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout


from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import redirect
from django.urls import reverse_lazy



def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in the user after registration
            return redirect('home')  # Redirect to the desired URL after successful registration
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')


def home(request):
    if request.user.is_authenticated:
        return redirect(reverse_lazy('IdeaBoards:IdeaBoards_Home'))
    else:
        return render(request, 'home.html')