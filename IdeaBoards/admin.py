from django.contrib import admin
from .models import IdeaBoard, IdeaBoardItem, ItemLabel, BoardComment

# Register your models here.
admin.site.register(IdeaBoard)
admin.site.register(IdeaBoardItem)
admin.site.register(ItemLabel)
admin.site.register(BoardComment)