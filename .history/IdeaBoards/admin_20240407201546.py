from django.contrib import admin
from .models import IdeaBoard, IdeaBoardItem

# Register your models here.
admin.site.register(IdeaBoard)
admin.site.register(IdeaBoardItem)
