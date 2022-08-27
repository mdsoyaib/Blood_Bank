from django.contrib import admin
from app.models import Blood, CustomUser, City, Event, EventRegistration, Feedback, ContactForm, BloodRequest, FeedbackLike, RequestToDonor, Donation

# Register your models here.

admin.site.register(Blood)
admin.site.register(CustomUser)
admin.site.register(City)
admin.site.register(Event)
admin.site.register(EventRegistration)
admin.site.register(Feedback)
# admin.site.register(FeedbackLike)
@admin.register(FeedbackLike)
class FeedbackLikeAdmin(admin.ModelAdmin):
    list_display = ("user", "feedback")
    list_per_page = 10

admin.site.register(ContactForm)
admin.site.register(BloodRequest)
# admin.site.register(RequestToDonor)
@admin.register(RequestToDonor)
class RequestToDonorAdmin(admin.ModelAdmin):
    list_display = ("id", "from_patient", "to_donor", "blood", "message", "created_at")
    list_per_page = 10

admin.site.register(Donation)
