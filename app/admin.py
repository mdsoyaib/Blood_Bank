from django.contrib import admin
from app.models import Blood, CustomUser, City, Event, EventRegistration, Feedback, ContactForm, BloodRequest, FeedbackLike, RequestToDonor

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

admin.site.register(ContactForm)
admin.site.register(BloodRequest)
admin.site.register(RequestToDonor)
