from django.urls import path
from . import views  # Import views correctly



urlpatterns = [
    path('', views.home, name='home'),
    path('sign_up/', views.sign_up_user, name='sign_up'),
    path('login/', views.login_user, name='login'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('reset-password/', views.reset_password, name='reset_password'),
    

    path('logout', views.logout_user, name='logout'),


    path("get_news_updates/", views.get_news_updates, name="get_news_updates"),

    path('contact/', views.contact_view, name='contact'),
]

