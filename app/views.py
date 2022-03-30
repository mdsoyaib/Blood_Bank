from django.shortcuts import render, redirect
from django.views import View
from app.models import City, Blood, CustomUser, Event, EventRegistration, Feedback, ContactForm, BloodRequest
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.db.models import F

# Create your views here.

# homepage view

class Home(View):
    def get(self, request):
        return render(request, 'home.html')


# blood bank page view

class BloodBank(View):
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            blood = Blood.objects.all()
            return render(request, 'blood_bank.html', {'blood':blood})
        else:
            messages.warning(request, "Login first to access that page")
            return redirect('login')

    def post(self, request):
        user = request.user
        blood = request.POST['bloodID']
        quantity = request.POST['quantity']
        quantity = int(quantity)
        checkBlood = Blood.objects.get(id=blood)

        if checkBlood.stock >= quantity:
            brequest = BloodRequest(blood=checkBlood, user=user, amount=quantity)
            brequest.save()
            checkBlood.stock = checkBlood.stock - quantity
            checkBlood.save()
            messages.success(request, "Your blood request is successfull. Collect the blood from blood bank!")
            return redirect('blood_requests')
        else:
            messages.warning(request, "Sorry! We don't have enough stock!")
            return redirect('blood_bank')


# blood request history page view

class BloodRequestHistory(View):
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            brequest = BloodRequest.objects.filter(user=user).order_by('-id')
            return render(request, 'blood_request_history.html', {'brequest':brequest})
        else:
            messages.warning(request, "Login first to access that page")
            return redirect('login')


# blood request report page view

class BloodRequestReport(View):
    def get(self, request, pk):
        user = request.user
        if user.is_authenticated:
            report = None
            
            try:
                report = BloodRequest.objects.get(id=pk, user=user)
                if user == report.user: 
                    return render(request, 'blood_request_report.html', {'report':report})
            except:
                report = None
                messages.warning(request, "you don't have access to that page")
                return redirect('blood_requests')

        else:
            messages.warning(request, "Sorry! you are not logged in!")
            return redirect('login')


# events page view

class Events(View):
    def get(self, request):
        event = Event.objects.all().order_by('-id')
        count = EventRegistration.objects.all()
        return render(request, 'event.html', {'event':event, 'count':count})

    def post(self, request):
        user = request.user
        if user.is_authenticated:

            event = request.POST['eventID']
            checkEvent = Event.objects.get(id=event)

            try:
                if EventRegistration.objects.all().get(event=checkEvent, user=user):
                    messages.warning(request, "You have already registered for this event")
                    return redirect('event')
            except:
                pass

            registration = EventRegistration(event=checkEvent, user=user)
            registration.save()

            messages.success(request, "Your registration for this event is successfull!")
            return redirect('event')
        else:
            messages.warning(request, "Login first to register in this event!")
            return redirect('login')


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


# feedback page view

class Feedbacks(View):
    def get(self, request):
        feedback = Feedback.objects.all().order_by('-id')
        return render(request, 'feedback.html', {'feedback': feedback})

    def post(self, request):
        user = request.user
        if user.is_authenticated:
            comment = request.POST['feedback']

            if comment == '':
                messages.warning(request, "please write something first and then submit feedback.")
                return redirect('feedback')
            
            else:
                feedback = Feedback(name=user.first_name + ' ' + user.last_name, feedback=comment)
                feedback.save()
                messages.success(request, 'Thanks for your feedback!')
                return redirect('feedback')

        else:
            messages.warning(request, "Please login first to post feedback.")
            return redirect('feedback')


# about us page view

class About(View):
    def get(self, request):
        return render(request, 'about_us.html')

    def post(self, request):
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']

        if name == '' or email == '' or message == '':
            messages.warning(request, 'Please fillup all the fields to send message!')
            return redirect('about')
        
        else:
            form = ContactForm(name=name, email=email, message=message)
            form.save()
            messages.success(request, 'You have successfully sent the message!')  
            return redirect('about')

