
from email import message
from multiprocessing import context
from django.shortcuts import render ,redirect
from .models import *
from .forms  import *
from django.contrib import messages
from django.views import generic
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request,'dashboard/home.html')
@login_required
def notes(request):
    if request.method == "POST":
        form =NotesForm(request.POST)
        if form.is_valid():
            notes = Notes(user=request.user,title=request.POST['title'],description=request.POST['description'])
            notes.save()

        messages.success(request,f"Notes Added from  {request.user.username}Sucessfully!")    
    form = NotesForm()
    notes=Notes.objects.filter(user=request.user)
    context={'notes':notes,'form':form}
    return render(request,'dashboard/notes.html',context)

def delete_note(request,pk=None):
    Notes.objects.get(id=pk).delete()
    return redirect("notes")

class NotesDetailView(generic.DetailView):
    model = Notes  

@login_required
def homework(request):
    homework=Homework.objects.filter(user=request.user)
    context={'homeworks':homework}
    return render(request,'dashboard/homework.html',context) 


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f"Account Create for {username}!!")
            return redirect("login")
    else:        
        form = UserRegistrationForm()
    context ={
        'form':form
    }
    return render(request,"dashboard/register.html",context)