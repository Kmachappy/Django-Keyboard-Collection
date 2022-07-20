from django.contrib import admin
from .models import Keyboard, Cleaning, Part

# Register your models here.
admin.site.register(Keyboard)
admin.site.register(Cleaning)
admin.site.register(Part)