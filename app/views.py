from django.shortcuts import render, redirect
from django.views import View
from app.models import City, Blood, CustomUser, Event, EventRegistration, Feedback, ContactForm, BloodRequest, FeedbackLike, RequestToDonor, Donation
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


# delete blood request view

class DeleteBloodRequest(View):
    def post(self, request):
        id = request.POST['requestID']

        deleteRequest = BloodRequest.objects.get(id=id)
        deleteRequest.delete()

        # when user deleting the request that blood stock will restock again
        checkBlood = Blood.objects.get(id=deleteRequest.blood.id)
        checkBlood.stock = checkBlood.stock + deleteRequest.amount
        checkBlood.save()
        
        messages.success(request, "You have successfully deleted the request!")
        return redirect('blood_requests')


# find donor page view

class FindDonor(View):
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            city = City.objects.all()
            blood = Blood.objects.all()
            if request.GET:
                checkCity = request.GET.get('city')
                checkBlood = request.GET.get('blood')
                donor = CustomUser.objects.filter(city=checkCity, blood=checkBlood, role="donor")
                return render(request, "find_donor.html", {'city':city, 'blood':blood, 'donor':donor})
            else:
                donor = CustomUser.objects.filter(role="donor")
                return render(request, "find_donor.html", {'city':city, 'blood':blood, 'donor':donor})
        else:
            messages.warning(request, "login first to access that page")
            return redirect('login')

    def post(self, request):
        user = request.user
        donor = request.POST['donorID']
        print(donor)
        blood = request.POST['blood']
        message = request.POST['message']

        checkDonor = CustomUser.objects.get(id=donor)
        checkBlood = Blood.objects.get(group=blood)

        requests = RequestToDonor(from_patient=user, to_donor=checkDonor, blood=checkBlood, message=message)
        requests.save()
        messages.success(request, "Check the donor contact number you requested and contact him/her for your needs.")
        return redirect('donor_requests')


# donor request history page view

class DonorRequestHistory(View):
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            requests = RequestToDonor.objects.filter(from_patient=user).order_by('-id')
            return render(request, "donor_request_history.html", {'request':requests})
        else:
            messages.warning(request, "login first to access that page")
            return redirect('login')


# patient request history page view

class PatientRequestHistory(View):
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            if user.role == "donor":
                requests = RequestToDonor.objects.filter(to_donor=user).order_by('-id')
                return render(request, "patient_request_history.html", {'request':requests})
            else:
                messages.warning(request, "you don't have access to this page")
                return redirect('home')
        else:
            messages.warning(request, "login first to access that page")
            return redirect('login')


#donate blood page view from where donor will register for donation

class DonateBlood(View):
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            if user.role == 'donor':
                check = Donation.objects.all()
                check = list(check)
                print(check[-1])
                return render(request, "donate_blood.html")
            else:
                messages.warning(request, 'update yourself from patient to donor for donating blood')
                return redirect('home')
        else:
            messages.warning(request, "login first to access that page")
            return redirect('login')

    def post(self, request):
        user = request.user
        
        check = Donation.objects.all()
        check = list(check)
        if check[-1].status == 'Pending':
            messages.warning(request, "You have already registerd for donation. Please check your last registration.")
            return redirect('donation_history')
        else:
            donation = request.POST['donation']
            donate = Donation(donor=user, donation=donation)
            donate.save()
            messages.success(request, "Registration for blood donation is successfull. Come to the blood bank to donate your blood.")
            return redirect('donation_history')


#donation history page view

class DonationHistory(View):
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            donation = Donation.objects.filter(donor=user)
            return render(request, 'donation_history.html', {'donation':donation})
        else:
            messages.warning(request, 'login first to access that page!')
            return redirect('login')


# cancel donation registration view

class CancelDonation(View):
    def post(self, request):
        id = request.POST['donationID']
        cancelDonation = Donation.objects.get(id=id)
        cancelDonation.delete()       
        messages.success(request, "You have successfully canceled donation registration!")
        return redirect('donation_history')


# events page view

class Events(View):
    def get(self, request):
        event = Event.objects.all().order_by('-id')
        return render(request, 'event.html', {'event':event})

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
            checkEvent.registration = checkEvent.registration + 1
            checkEvent.save()

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
        user=request.user
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
                
                try:
                    if Feedback.objects.all().get(user=user):
                        messages.warning(request, "You have given feedback earlier!")
                        return redirect('feedback')
                except:
                    pass    

                feedback = Feedback(user=user, feedback=comment)
                feedback.save()
                messages.success(request, 'Thanks for your feedback!')
                return redirect('feedback')

        else:
            messages.warning(request, "Please login first to post feedback.")
            return redirect('feedback')


# edit feedback view

class EditFeedback(View):
    def post(self, request, id):
        user = request.user
        editFeedback = request.POST['editFeedback']
        
        if editFeedback == '':
            messages.warning(request, "You haven't written aything.")
            return redirect('feedback')
        else:
            update = Feedback.objects.get(id=id, user=user)
            update.feedback = editFeedback
            update.save()
            messages.success(request, "Your feedback updated successfully!")
            return redirect('feedback')


# delete feedback view

class DeleteFeedback(View):
    def post(self, request, id):
        feedback = Feedback.objects.get(id=id)
        feedback.delete()
        messages.success(request, "Your feedback has been deleted.")
        return redirect('feedback')


# feedback like view

class LikeFeedback(View):
    def post(self, request, id):
        user = request.user
        check = Feedback.objects.get(id=id)
        try:
            if FeedbackLike.objects.all().get(user=user, feedback=check):
                messages.warning(request, "You have already liked this feedback")
                return redirect('feedback')
        except:
            pass

        flike = FeedbackLike(user=user, feedback=check)
        flike.save()
        check.like = check.like + 1
        check.save()
        messages.success(request, "Thanks for your like!")
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

