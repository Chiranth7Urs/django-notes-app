from django.shortcuts import render, redirect, get_object_or_404
from .models import Note

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required


# ================= NOTES =================

@login_required
def note_list(request):
    notes = Note.objects.all().order_by('-created_at')
    return render(request, 'notes/note_list.html', {'notes': notes})


@login_required
def add_note(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        Note.objects.create(title=title, content=content)
        return redirect('note_list')

    return render(request, 'notes/add_note.html')


@login_required
def edit_note(request, id):
    note = get_object_or_404(Note, id=id)

    if request.method == 'POST':
        note.title = request.POST['title']
        note.content = request.POST['content']
        note.save()
        return redirect('note_list')

    return render(request, 'notes/edit_note.html', {'note': note})


@login_required
def delete_note(request, id):
    note = get_object_or_404(Note, id=id)
    note.delete()
    return redirect('note_list')


# ================= AUTH =================

def user_login(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('note_list')

    return render(request, 'notes/login.html')


def user_logout(request):
    logout(request)
    return redirect('login')


def register(request):

    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')

    return render(request, 'notes/register.html', {'form': form})
