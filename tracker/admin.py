from .models import Uploads
from django.contrib import admin

@admin.register(Uploads)
class Uploads(admin.ModelAdmin):
    list_display=['id','image']