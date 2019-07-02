from django.contrib import admin
from contacts.models import User, Contact
from django.contrib.auth.admin import UserAdmin

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Contact)