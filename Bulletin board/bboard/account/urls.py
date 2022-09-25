from django.urls import path
from .views import profile,RegisterUserViews,ActivationView
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('profile/', profile, name='profile'),
    path('login/',
         LoginView.as_view(template_name='account/login.html'),
         name='login'),
    path('profile/logout/',
         LogoutView.as_view(template_name='account/logout.html'),
         name='logout'),
    path('signup/',
         RegisterUserViews.as_view(template_name='account/signup.html'),
         name='signup'),
    path('signup/otp_code/', ActivationView.as_view(),name='otp_code'),

]