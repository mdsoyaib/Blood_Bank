"""blood_bank URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app.views import Home, Signup, Login, Events, Feedbacks, About, BloodBank, BloodRequestHistory, BloodRequestReport, DeleteBloodRequest, EditFeedback, DeleteFeedback, LikeFeedback, FindDonor, DonorRequestHistory
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', Home.as_view(), name="home"),
    path('blood_bank', BloodBank.as_view(), name="blood_bank"),
    path('find_donor', FindDonor.as_view(), name="find_donor"),
    path('donor_requests', DonorRequestHistory.as_view(), name="donor_requests"),
    path('event', Events.as_view(), name="event"),

    path('feedback', Feedbacks.as_view(), name="feedback"),
    path('edit_feedback/<int:id>', EditFeedback.as_view(), name="edit_feedback"),
    path('delete_feedback/<int:id>', DeleteFeedback.as_view(), name="delete_feedback"),
    path('like_feedback/<int:id>', LikeFeedback.as_view(), name="like_feedback"),

    path('about', About.as_view(), name="about"),

    path('blood_requests', BloodRequestHistory.as_view(), name="blood_requests"),
    path('blood_requests/report/<int:pk>', BloodRequestReport.as_view(), name="blood_request_report"),
    path('delete_blood_request', DeleteBloodRequest.as_view(), name="delete_blood_request"),

    path('login', Login.as_view(), name="login"),
    path('signup', Signup.as_view(), name="signup"),
    path('logout', auth_views.LogoutView.as_view(), name="logout"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
