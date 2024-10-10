from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import customer, restaurant , comments ,Leaderborad_backup # Import your model

admin.site.register(restaurant)  # Register your model
admin.site.register(comments) 
admin.site.register(customer) 
admin.site.register(Leaderborad_backup)
