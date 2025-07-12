from django.contrib import admin

from .models import ContactMessage, PasswordResetOTP # Import your model here

admin.site.register(ContactMessage)
admin.site.register(PasswordResetOTP)
