# middleware.py
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect, render
from .models import LicenseKey
from django.contrib import messages
class LicenseCheckMiddleware(MiddlewareMixin):
    def process_request(self, request):
        try:
            license_key = LicenseKey.objects.get(is_active=True)
            if license_key.has_expired():
                license_key.is_active = False  # Mark license as inactive
                license_key.save()
                messages.error(request,"Expired License key")
                return render(request,"license_expired.html")  # Redirect to an expiry page
        except LicenseKey.DoesNotExist:
            messages.error(request,"No License key") 
            return render(request,"no_license.html")  # Redirect to an expiry page
             # Redirect if no valid license key is found
