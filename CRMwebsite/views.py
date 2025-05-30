from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import signUpForm, AddRecordForm
from .models import Record


# Create your views here.
def home(request):
    records = Record.objects.all()
    
    #check if the user loggin in
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get('password')
        #authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been successfully logged In!")
            return redirect(home)
        else:
            messages.success(request, "Web couldn't log you in. Try again")
            return redirect('home')
    return render(request, 'home.html', {'records':records})


def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out...")
    return redirect('home')


def register_user(request):
    if request.method == "POST":
        form = signUpForm(request.POST)
        if form.is_valid():
            form.save()
            #authenticate and login
            username  = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You have been registered!")
            return redirect('home')
    else:
        form = signUpForm()
        return render(request, 'register.html', {'form':form})
    return render(request, 'register.html', {'form':form})

def customer_record(request, pk):
    if request.user.is_authenticated:
        customer_record = Record.objects.get(id=pk)
        return render(request, 'record.html', {"customer_record":customer_record})
    else:
        messages.success(request, "You need to login in order to see the record page")
        return redirect("home")

def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_item = Record.objects.get(id=pk)
        delete_item.delete()
        messages.success(request, "Record deleted successfully")
        return redirect("home")
    else:
        messages.success(request, "Sorry, you need to login in order to delete this record!")
        return redirect("home")

def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method ==  "POST":
           if form.is_valid():
               add_record = form.save()
               messages.success(request, "Record Added")
               return redirect('home') 
        return render(request, 'add_record.html', {"form": form})
    else:
        messages.success(request, "You must be logged in")
        return redirect("home")

def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, "Record has been updated!")
            return redirect('home')
        else:
            return render(request, "update_record.html", {"form":form})
    else:
        messages.success(request, "You need to log In so you can access this page")
        return redirect('home', {"form":form})