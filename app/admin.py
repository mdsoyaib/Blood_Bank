from django.contrib import admin
from app.models import Blood, CustomUser, City, Event, EventRegistration

# Register your models here.

admin.site.register(Blood)
admin.site.register(CustomUser)
admin.site.register(City)
admin.site.register(Event)
admin.site.register(EventRegistration)
