from django.contrib import admin

from .models import comments, newitem

admin.site.register(newitem)
admin.site.register(comments)
