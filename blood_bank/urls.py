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
from app.views import Home, Signup, Login, Events, Feedbacks, About
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Home.as_view(), name="home"),
    path('event', Events.as_view(), name="event"),
    path('feedback', Feedbacks.as_view(), name="feedback"),
    path('about', About.as_view(), name="about"),

    path('login', Login.as_view(), name="login"),
    path('signup', Signup.as_view(), name="signup"),
    path('logout', auth_views.LogoutView.as_view(), name="logout"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
