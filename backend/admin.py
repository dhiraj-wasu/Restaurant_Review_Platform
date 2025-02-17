from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import restaurant , comments ,Leaderborad_backup,M_User  # Import your model

admin.site.register(restaurant)  # Register your model
admin.site.register(comments) 
admin.site.register(M_User) 
admin.site.register(Leaderborad_backup)
