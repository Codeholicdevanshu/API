from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(Registeruser)
class AdminRegister(admin.ModelAdmin):
    list_display = ['id','firstname','lastname','email','password']
