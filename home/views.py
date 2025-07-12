from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from dashboard.models import UserProfile  # User financial data ke liye

def home(request):
    # Safely retrieve and remove 'open_modal' from session for one-time use
    modal_to_open = request.session.pop('open_modal', None)
    return render(request, 'home.html', {'open_modal': modal_to_open})
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from dashboard.models import UserProfile




def sign_up_user(request):
    if request.method == "POST":
        full_name = request.POST.get('full_name', '').strip()
        if not full_name:
            messages.error(request, "Full name is required.")
            return render(request, 'sign_up.html')

        name_parts = full_name.split()
        first_name = name_parts[0]
        last_name = " ".join(name_parts[1:]) if len(name_parts) > 1 else ''

        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        mobile = request.POST.get('mobile', '').strip()
        dob = request.POST.get('dob', '').strip()
        gender = request.POST.get('gender', '').strip()
        savings = request.POST.get('savings', '').strip()
        existing_investments = request.POST.get('existing_investments', '').strip()
        risk_appetite = request.POST.get('risk_appetite', '').strip()
        investment_goals = request.POST.get('investment_goals', '').strip()

        if User.objects.filter(username=email).exists():
            messages.error(request, "⚠️ Email already registered! Please try logging in.")
            return render(request, 'sign_up.html', {
                'full_name': full_name,
                'email': email,
                'mobile': mobile,
                'dob': dob,
                'gender': gender,
                'savings': savings,
                'existing_investments': existing_investments,
                'risk_appetite': risk_appetite,
                'investment_goals': investment_goals,
            })

        user = User.objects.create_user(username=email, email=email, password=password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        UserProfile.objects.create(
            user=user,
            mobile=mobile,
            dob=dob,
            gender=gender,
            savings=savings,
            existing_investments=existing_investments,
            risk_appetite=risk_appetite,
            investment_goals=investment_goals,
        )

        # Success message for display and auto redirect
        messages.success(request, f"🎉 Congratulations {first_name}! Your account has been successfully created. Redirecting to login page...")

        return render(request, 'sign_up.html', {
            'redirect_to_login': True
        })

    return render(request, 'sign_up.html')


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages


def login_user(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "❌ Invalid login details.")
            return redirect('login')  # stay on login page and show error

    # If GET request, render the login page
    return render(request, 'login.html')


from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
import random
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from .models import PasswordResetOTP  # Assuming your model is in the same app

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            otp = str(random.randint(100000, 999999))
            PasswordResetOTP.objects.filter(user=user).delete()
            PasswordResetOTP.objects.create(user=user, otp=otp)

            subject = 'Personal Finance Advisor: Password Reset OTP'
            message = f"""Dear {user.first_name},

You have requested to reset the password for your Personal Finance Advisor account associated with the email address {email}. Your One-Time Password (OTP) for password reset is: {otp} Please enter this OTP on the password reset page. This OTP is valid for the next 5 minutes. If you did not request this password reset, please ignore this email. Your account remains secure.
Thank you,
The Personal Finance Advisor Team
"""
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [email]

            send_mail(subject, message, from_email, recipient_list)
            request.session['reset_user_id'] = user.id
            return JsonResponse({'status': 'otp_sent', 'email': email})
        except User.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'No user found with that email address.'}, status=404)
    return render(request, 'forgot_password.html')

def verify_otp(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if 'reset_user_id' not in request.session:
            return JsonResponse({'status': 'error', 'message': 'Invalid request. Please try forgot password again.'}, status=400)

        user_id = request.session['reset_user_id']
        try:
            user = User.objects.get(id=user_id)
            otp_entered = request.POST.get('otp')
            otp_record = PasswordResetOTP.objects.filter(user=user, otp=otp_entered).first()
            if otp_record:
                if (timezone.now() - otp_record.created_at).total_seconds() < 300:
                    request.session['verified_user_id'] = user.id
                    PasswordResetOTP.objects.filter(user=user).delete() # Delete on successful verification
                    return JsonResponse({'status': 'success'})
                else:
                    otp_record.delete() # Delete expired OTP
                    return JsonResponse({'status': 'error', 'message': 'OTP has expired. Please request a new one.'}, status=400)
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid OTP. Please try again.'}, status=400)
        except User.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Invalid user session.'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request.'}, status=400)

def reset_password(request):
    if 'verified_user_id' not in request.session:
        messages.error(request, 'Invalid request. Please verify OTP first.')
        return redirect('forgot_password')

    user_id = request.session['verified_user_id']
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, 'Invalid user session.')
        return redirect('forgot_password')

    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        if new_password == confirm_password:
            user.set_password(new_password)
            user.save()
            del request.session['verified_user_id']
            messages.success(request, 'Password reset successfully! You can now log in.')
            return redirect('login')
        else:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'forgot_password.html', {'show_reset_form': True})
    else:
        return render(request, 'forgot_password.html', {'show_reset_form': True})



def logout_user(request):
    logout(request)
    return redirect('home')




import requests
import random
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def get_news_updates(request):
    try:
        FINNHUB_API = "https://finnhub.io/api/v1/news?category=general&token=cvhd29pr01qrtb3nse20cvhd29pr01qrtb3nse2g"
        API_URL = FINNHUB_API  

        response = requests.get(API_URL)
        data = response.json()

        latest_news = []
        if isinstance(data, list):
            # ✅ Randomly select 3 unique news articles
            random_articles = random.sample(data, min(3, len(data)))
            for article in random_articles:
                latest_news.append({
                    "title": article.get("headline", "No Title"),
                    "description": article.get("summary", "No description available."),
                    "url": article.get("url", "#"),
                })

        unread_count = len(latest_news)

        return JsonResponse({"unread_count": unread_count, "news": latest_news})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)









from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import ContactMessage

@csrf_exempt
def contact_view(request):
    if request.method == "POST":
        try:
            # Extracting data from the request
            name = request.POST.get("name")
            phone = request.POST.get("phone")
            email = request.POST.get("email")
            subject = request.POST.get("subject")
            message = request.POST.get("message")

            # Ensure all fields are provided
            if not all([name, phone, email, subject, message]):
                return JsonResponse({
                    "success": False,
                    "message": "All fields are required."
                })

            # Save the contact message to the database
            ContactMessage.objects.create(
                name=name,
                phone=phone,
                email=email,
                subject=subject,
                message=message
            )

            # Return success response
            return JsonResponse({
                "success": True,
                "message": "Thank you for reaching out! Your message has been successfully sent, and our team will get back to you shortly."
            })

        except Exception as e:
            # Return error response in case of exception
            return JsonResponse({
                "success": False,
                "message": f"An error occurred while sending your message: {str(e)}"
            })

    # If the request method is not POST
    return JsonResponse({
        "success": False,
        "message": "Invalid request method. Please use POST."
    })
