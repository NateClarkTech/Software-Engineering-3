from django.contrib import admin

from .models import Thread, Page, Comment, Notification

# Register your models here.
admin.site.register(Thread)
admin.site.register(Page)
admin.site.register(Comment)
admin.site.register(Notification)   