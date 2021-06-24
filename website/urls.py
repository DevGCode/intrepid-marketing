from django.urls import path, include
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views

urlpatterns = [
    # signup
    path('signup/', UserSignupView.as_view(), name='signup'),
    path("signin/", signin, name="signin"),
    path("signout/", signout, name="signout"),
    # blog
    path('search/', search, name='search'),
    path('blog/', posts, name='post-list'),
    path('post/<str:pk>/', post_detail, name='post-detail'),
    path('contact/', contact, name='contact'),
    path('request-portfolio/', portfolio, name="request-portfolio"),
    # terms & privacy
    path('terms/', terms, name='terms'),
    path('privacy/', privacy, name='privacy'),
    # estimate section
    path('free-website-audit/', audit, name='free-website-audit'),
    # new listing
    path('submit-info/', submit_info, name='submit-info'),
    # website categories/locations
    path('post-category/<str:cats>/', post_category_detail, name='post-category-detail'),
    path('service/<str:cats>/', service_detail, name='service-detail'),
]
