from django.shortcuts import render, redirect
from django.views import View
from app.models import City, Blood, CustomUser, Event
from django.contrib import messages
from django.contrib.auth import authenticate, login

# Create your views here.

# homepage view

class Home(View):
    def get(self, request):
        return render(request, 'home.html')


# events page view

class Events(View):
    def get(self, request):
        event = Event.objects.all().order_by('-id')
        return render(request, 'event.html', {'event':event})


# signup page view for donor and patient

class Signup(View):
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            return redirect('home')
        else:
            city = City.objects.all()
            blood = Blood.objects.all()
            return render(request, 'signup.html', {'city':city, 'blood':blood})

    def post(self, request):
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        phone = request.POST['phone']   
        city = request.POST['city']  
        role = request.POST['role']
        blood = request.POST['blood']  
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.warning(request,"Password didn't matched")
            return redirect('signup')

        elif city == 'Select':
            messages.warning(request,"Please select a city")
            return redirect('signup')

        elif blood == 'Choose':
            messages.warning(request,"Please choose a blood group")
            return redirect('signup')
        
        try:
            if CustomUser.objects.all().get(username=username):
                messages.warning(request,"username not Available")
                return redirect('signup')

        except:
            pass            

        new_user = CustomUser.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, phone=phone, city=city, role=role, blood=blood, password=password1)
        new_user.is_superuser=False
        new_user.is_staff=False
            
        new_user.save()
        messages.success(request,"Registration Successfull")
        return redirect("login")


# login page view for admin, donar, patient

class Login(View):
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            return redirect('home')
        else:
            return render(request, 'login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username,password=password)
        
        if user is not None:
            login(request,user)
            messages.success(request,"successful logged in")
            return redirect('home')
        else:
            messages.warning(request,"Incorrect username or password")
            return redirect('login')

