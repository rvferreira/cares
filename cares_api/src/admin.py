from django.contrib import admin

# Register your models here.

from .models import User, Ticket, Topic, Career, TicketInsideCareer, Enrollment, Sprint

admin.site.register(User)
admin.site.register(Ticket)
admin.site.register(Topic)
admin.site.register(Career)
admin.site.register(TicketInsideCareer)
admin.site.register(Enrollment)
admin.site.register(Sprint)