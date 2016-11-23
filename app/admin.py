from django.contrib import admin

# Register your models here.

from . import models

admin.site.register(models.User)
admin.site.register(models.Topic)
admin.site.register(models.Ticket)
admin.site.register(models.Career)
admin.site.register(models.TicketInsideSprint)
admin.site.register(models.Enrollment)
admin.site.register(models.Sprint)

