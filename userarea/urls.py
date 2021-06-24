from .views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views

urlpatterns = [
    # User dashboard
    path('user-profile/', login_required(user_profile), name='user-profile'),
    path('user-billing/', login_required(user_billing), name='user-billing'),
    path('user-reports/', login_required(user_reports), name='user-reports'),
    path('user-support/', login_required(user_support), name='user-support'),
    path('ticket/<int:pk>/', login_required(ticket), name='ticket'),
    path('add-ticket-response/<int:pk>/', login_required(add_ticket_response), name='add-ticket-response'),
    path('mark-ticket-as-read/<int:pk>/', login_required(read_ticket), name='mark-ticket-as-read'),
    path('update-profile/', login_required(update_profile), name="update-profile"),
    path('mark-billing-as-read/<int:pk>/', login_required(read_billing), name='mark-billing-as-read'),
    path('update-info/<pk>', login_required(UpdateWebsiteInfoView.as_view()), name="update-info"),
    path('update-profile/', login_required(UserEditView.as_view()), name="update-profile"),
    path('info/<pk>/', login_required(info_detail), name='info-detail'),
    # update password
    path('password-changed/', login_required(password_changed), name='password-changed'),
    path('password/', login_required(PasswordsChangeView.as_view(template_name="user/change-password.html")), name='info-detail'),
    # referrals
    path('referrals/', login_required(referrals), name="referrals"),
    path('referral/<int:pk>', login_required(referral), name="referral"),
    path('mark-referral-as-read/<int:pk>/', login_required(read_referral), name='mark-referral-as-read'),
]
