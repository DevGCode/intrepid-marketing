from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import *
from django.conf import settings
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import *
from django.shortcuts import render, redirect
from django.db.models import Count, Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.http import HttpResponseRedirect
from django.views import generic
import json
import requests
from adminarea.models import *

# Website
nav_services = Service.objects.all()

# Referral counter
current_promo = Promo.objects.filter(current=True)



def terms(request):
    return render(request, 'compliance/terms_of_service.html', {})



def privacy(request):
    return render(request, 'compliance/privacy_policy.html', {})



class IndexView(View):

    def get(self, request, *args, **kwargs):
        featured = Post.objects.filter(featured=True)
        latest = Post.objects.order_by('-timestamp')[0:3]

        context = {
            'nav_services':nav_services,
            'object_list': featured,
            'latest': latest,
        }
        return render(request, 'index.html', context)

    def post(self, request, *args, **kwargs):
        email = request.POST.get("email")
        new_signup = Signup()
        new_signup.email = email
        new_signup.save()
        messages.info(request, "Successfully subscribed")
        return redirect("home")



def index(request):
    featured = Post.objects.filter(featured=True)
    latest = Post.objects.order_by('-timestamp')[0:3]

    if request.method == "POST":
        email = request.POST["email"]
        new_signup = Signup()
        new_signup.email = email
        new_signup.save()

    context = {
        'nav_services':nav_services,
        'object_list': featured,
        'latest': latest,
        'form': form
    }
    return render(request, 'index.html', context)



@login_required(login_url='signup')
def submit_info(request):
    if request.method == "POST":
        business_name = request.POST['business_name']
        tagline = request.POST['tagline']
        description = request.POST['description']
        address = request.POST['address']
        phone = request.POST['phone']
        email = request.POST['email']
        website = request.POST['website']

        # Get the opening hours
        mondayopen = request.POST['mondayopen']
        tuesdayopen = request.POST['tuesdayopen']
        wednesdayopen = request.POST['wednesdayopen']
        thursdayopen = request.POST['thursdayopen']
        fridayopen = request.POST['fridayopen']
        saturdayopen = request.POST['saturdayopen']
        sundayopen = request.POST['sundayopen']
        # Get the closing hours
        mondayclosed = request.POST['mondayclosed']
        tuesdayclosed = request.POST['tuesdayclosed']
        wednesdayclosed = request.POST['wednesdayclosed']
        thursdayclosed = request.POST['thursdayclosed']
        fridayclosed = request.POST['fridayclosed']
        saturdayclosed = request.POST['saturdayclosed']
        sundayclosed = request.POST['sundayclosed']

        # Get users info
        user = request.user

        # Store the listing
        website_info = WebsiteInfo.objects.create(
        user=user,
        business_name=business_name,
        tagline=tagline,
        description=description,
        address=address,
        phone=phone,
        email=email,
        website=website,
        )

        # Store the hours
        new_hours = BusinessHours.objects.create(
        monday_open=mondayopen,
        monday_closed=mondayclosed,
        tuesday_open=tuesdayopen,
        tuesday_closed=tuesdayclosed,
        wednesday_open=wednesdayopen,
        wednesday_closed=wednesdayclosed,
        thursday_open=thursdayopen,
        thursday_closed=thursdayclosed,
        friday_open=fridayopen,
        friday_closed=fridayclosed,
        saturday_open=saturdayopen,
        saturday_closed=saturdayclosed,
        sunday_open=sundayopen,
        sunday_closed=sundayclosed,
        website_info=website_info,
        )

        # Store the faqs
        faqs = request.POST.getlist('faqs')
        faqanswers = request.POST.getlist('faqanswers')

        i = 0

        for faq in faqs:
            FrequentlyAskedQuestion.objects.create(website_info=website_info, question=faq, answer=faqanswers[i])
            i += 1


        context = {
            'website_info':website_info,
            'nav_services':nav_services,
        }


        return render(request, 'submit-info.html', context)

    context = {
        'nav_services':nav_services,
    }
    return render(request, 'submit-info.html', context)



def contact(request):
    if request.method == "POST":

        message_name = request.POST['name']
        message_url = request.POST['url']
        message_email = request.POST['email']
        message = request.POST['message']

        context = {
        'nav_services':nav_services,
        'message': message,
        'message_name':message_name
        }

        return render(request, 'contact.html', context)

    context = {
        'nav_services':nav_services,
    }
    return render(request, 'contact.html', context)



def portfolio(request):
    if request.method == "POST":

        message_name = request.POST['name']
        message_url = request.POST['url']
        message_email = request.POST['email']
        message = request.POST['message']


        context = {
        'nav_services':nav_services,
        'message': message,
        'message_name':message_name
        }

        return render(request, 'request-portfolio.html', context)

    context = {
        'nav_services':nav_services,
    }
    return render(request, 'request-portfolio.html', context)



def audit(request):

    if request.method == "POST":
        first_last = request.POST['firstlast']
        phone = request.POST['phone']
        website = request.POST['website']
        email_address = request.POST['email']

        phone_number = '+1' + phone

        # STORE APPLICATION IN DATABASE
        website_audit = WebsiteAudit.objects.create(
        website=website,
        name=first_last,
        phone=phone_number,
        email=email_address
        )

        context = {
        'nav_services':nav_services,
        'first_last': first_last
        }

        return render(request, 'free-website-audit.html', context)

    context = {
        'nav_services':nav_services,
    }
    return render(request, 'free-website-audit.html', context)



def service_detail(request, cats):

    service = Service.objects.get(id=cats)

    context = {
        'service':service,
        'nav_services':nav_services,

    }

    return render(request, 'service.html', context)



def post_category_detail(request, cats):
    categories = Category.objects.all()
    most_recent = Post.objects.order_by('-timestamp')[:3]

    cat_posts = Post.objects.filter(categories=cats)
    posts = Post.objects.all()
    category = categories.get(id=cats)

    context = {
        'most_recent':most_recent,
        'categories':categories,
        'cat_posts':cat_posts,
        'posts': posts,
        'category':category,
        'nav_services':nav_services,

    }

    return render(request, 'post-category.html', context)



def post_detail(request, pk):
    most_recent = Post.objects.order_by('-timestamp')[:3]
    post = Post.objects.get(id=pk)
    categories = Category.objects.all()

    context = {
        'categories':categories,
        'post': post,
        'most_recent': most_recent,
        'nav_services':nav_services,
    }
    return render(request, 'post.html', context)



def posts(request):
    categories = Category.objects.all()
    posts = Post.objects.all()


    most_recent = Post.objects.order_by('-timestamp')[:3]

    context = {
        'most_recent':most_recent,
        'categories':categories,
        'posts': posts,
        'nav_services':nav_services,

    }
    return render(request, 'blog.html', context)



# def search(request):
#     if request.method == 'POST': # check post
#         form = SearchForm(request.POST)
#         if form.is_valid():
#             query = form.cleaned_data['query'] # get form input data
#             catid = form.cleaned_data['catid']
#             if catid==0:
#                 products=Product.objects.filter(title__icontains=query)  #SELECT * FROM product WHERE title LIKE '%query%'
#             else:
#                 products = Product.objects.filter(title__icontains=query,category_id=catid)

#             category = Category.objects.all()

#             context = {
#                 'products': products,
#                 'query':query,
#                 'category': category,
#                 'nav_services':nav_services,

#                 }
#             return render(request, 'search_results.html', context)

#     return HttpResponseRedirect('/')



# def search_auto(request):
#     if request.is_ajax():
#         q = request.GET.get('term', '')
#         products = Product.objects.filter(title__icontains=q)

#         results = []
#         for rs in products:
#             product_json = {}
#             product_json = rs.title +" > " + rs.category.title
#             results.append(product_json)
#         data = json.dumps(results)
#     else:
#         data = 'fail'
#     mimetype = 'application/json'
#     return HttpResponse(data, mimetype)



def get_author(user):
    qs = Author.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    return None



class SearchView(View):
    def get(self, request, *args, **kwargs):
        queryset = Post.objects.all()
        query = request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(overview__icontains=query)
            ).distinct()

        context = {
            'queryset': queryset,
            'nav_services':nav_services,
        }
        return render(request, 'search_results.html', context)



# Blog Post Search
def search(request):
    queryset = Post.objects.all()
    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(overview__icontains=query)
        ).distinct()

    context = {
        'queryset': queryset,
        'nav_services':nav_services,
    }

    return render(request, 'search_results.html', context)



def get_category_count():
    queryset = Post \
        .objects \
        .values('categories__title') \
        .annotate(Count('categories__title'))
    return queryset



# user signup / signin / signout
class UserSignupView(generic.CreateView):
    form_class = UserCreationForm
    template_name = 'signup.html'
    success_url = reverse_lazy('signin')



def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('user-profile')
        else:
            messages.info(request,"Username or Password is not correct.")
    return render(request, 'signin.html',{})



def signout(request):
    logout(request)
    return redirect('signin')
