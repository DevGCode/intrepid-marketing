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
from .filters import ProductFilter
from django.db.models import Count, Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.http import HttpResponseRedirect
from django.views import generic
import requests
from website.models import WebsiteAudit
from userarea.models import Deliverable, Report
from website.forms import ContactForm



################### ADMIN AREA #####################

@user_passes_test(lambda u: u.is_superuser)
def support_dashboard(request):
    if request.method == "POST":
        data = {}
        csv_file = request.FILES["csv_file"]
        # if not csv_file.name.endswith('.csv'):
        # messages.error(request,'File is not CSV type')
        file_data = csv_file.read().decode("utf-8")		
        lines = file_data.split("\n")
        # loop over the lines and save them in db. If error , store as string and then display
        for line in lines:						
            fields = line.split(",")
            if line:
                leads = Lead.objects.get_or_create(
                        name=fields[0],
                        city=fields[1],
                        business_name=fields[2],
                        business_type=fields[3],
                        url=fields[4],
                        phone_number=fields[5],
                        note=fields[6],
                        )
        
        context = {}
        csv = True
        context['leads'] = Lead.objects.order_by('-timestamp')
        return render(request, 'adminarea/support_dashboard.html', {})

    products = Product.objects.all()
    context = {'products':products}
    context['leads'] = Lead.objects.order_by('-timestamp')
    return render(request, 'adminarea/support_dashboard.html', context)

 

 
class UpdateLeadView(UpdateView):
    model = Lead
    template_name = 'adminarea/update-lead.html'
    form_class = UpdateLead
    success_url = reverse_lazy('dashboard')


class CreateLeadView(CreateView):
    model = Lead
    form_class = CreateLead
    template_name = 'adminarea/new-lead.html'
    success_url = reverse_lazy('dashboard')

    

@user_passes_test(lambda u: u.is_superuser)
def get_weather(request):
    if request.method == "POST":
        city = request.POST['weather_city']
            
        ### WEATHER ###
        url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid=8adeafa1da277ff64dfe8f1addfb3e36&units=imperial'.format(city)

        res = requests.get(url)

        data = res.json()

        todays_weather = data['weather'][0]['description'] 
        
        leads = Lead.objects.order_by('-timestamp')
        
        
        context = {
            'todays_weather':todays_weather,
            'leads':leads,
        } 
        return render(request, 'adminarea/support_dashboard.html', context)

    leads = Lead.objects.order_by('-timestamp')
        
    context = {
        'leads':leads,
    }  
    return render(request, 'adminarea/support_dashboard.html', context)




@user_passes_test(lambda u: u.is_superuser)
def remove_from_list(request, pk):
    lead = Lead.objects.get(id=pk)
    lead.call_list = False
    lead.save()

    leads = Lead.objects.order_by('-timestamp')
        
    context = {
        'leads':leads,
    }  
    return render(request, 'adminarea/support_dashboard.html', context)




@user_passes_test(lambda u: u.is_superuser)
def add_as_client(request, pk):
    lead = Lead.objects.get(id=pk)
    lead.customer = True
    lead.save()

    leads = Lead.objects.order_by('-timestamp')
        
    context = {
        'leads':leads,
    }  
    return render(request, 'adminarea/support_dashboard.html', context)

 


@user_passes_test(lambda u: u.is_superuser)
def create_response(request, pk):
    if request.method == "POST":
        # FILTER BY AGENT
        # Get the id from the selector field
        subject = request.POST['summary']
        description = request.POST['body']

        ticket = SupportTicket.objects.get(id=pk)

        Support_Ticket_Response.objects.create(
            ticket=ticket,
            user=ticket.user,
            subject=subject, 
            description=description
        )

        created = 'true'
            
        context = {
            'created':created,
            'ticket':ticket,
        }  
        return render(request, 'adminarea/create-response.html', context)

    ticket = SupportTicket.objects.get(id=pk)
            
    context = {
        'ticket':ticket,
    }  

    return render(request, 'adminarea/create-response.html', context)

 
 
@user_passes_test(lambda u: u.is_superuser)
def reports(request):
    if request.method == "POST":
        # FILTER BY AGENT
        # Get the id from the selector field
        agent_id_str = request.POST['agent']
        # Convert the agent type from str to int 
        agent_id_int = int(agent_id_str)
        # Grab the sales agent that matches that id
        agent = SalesAgent.objects.get(id=agent_id_int)
        # Find the leads that have that agent 
        agent_leads = Lead.objects.filter(agent=agent)
        # Get all agents for the selector field
        agents = SalesAgent.objects.all()
        # Get all leads for the bottom of the page
        leads = Lead.objects.all()

        # FILTER BY CLOSED
        closed = request.POST['closed']

        if closed == "1":
            closed_leads = Lead.objects.filter(customer=True)
            open_leads = False
        if closed == "2":
            open_leads = Lead.objects.filter(customer=False)
            closed_leads = False
    
        context = {  
        'closed_leads':closed_leads,
        'open_leads':open_leads,
        'agent':agent,
        'leads':leads,
        'agents':agents,
        'agent_leads':agent_leads,
        }

        return render(request, 'adminarea/report.html', context)

    leads = Lead.objects.all()
    agents = SalesAgent.objects.all()

    context = {  
    'agents':agents,
    'leads':leads,
    }

    return render(request, 'adminarea/report.html', context)



@user_passes_test(lambda u: u.is_superuser)
def toggle_product(request, cats):
    product_obj = Product.objects.get(id=cats)

    leads = Lead.objects.filter(product=product_obj).order_by('-timestamp')

    products = Product.objects.all()
        
    context = {
        'products':products,
        'leads':leads,
    }
    return render(request, 'adminarea/support_dashboard.html', context)



@user_passes_test(lambda u: u.is_superuser)
def website_leads(request):
    aduits = WebsiteAudit.objects.all()

    leads = aduits.order_by('-date_created')

    products = Product.objects.all()
        
    context = {
        'products':products,
        'leads':leads,
    }
    return render(request, 'adminarea/website_leads.html', context)


@user_passes_test(lambda u: u.is_superuser)
def client_leads(request):
    all_referrals = Referral.objects.all()

    referrals = all_referrals.order_by('-id')

    products = Product.objects.all()
        
    context = {
        'products':products,
        'referrals':referrals,
    }
    return render(request, 'adminarea/referral_leads.html', context)



###### SUPPORT SECTION FOR ADMIN ########


@user_passes_test(lambda u: u.is_superuser)
def tickets(request):
    tickets = SupportTicket.objects.filter(status='OPEN').order_by('-timestamp')

    products = Product.objects.all()
        
    context = {
        'tickets':tickets,
        'products':products,
    }
    return render(request, 'adminarea/tickets.html', context)


@user_passes_test(lambda u: u.is_superuser)
def paused_tickets(request):
    tickets = SupportTicket.objects.filter(status='PAUSED').order_by('-timestamp')

    products = Product.objects.all()
        
    context = {
        'tickets':tickets,
        'products':products,
    }
    return render(request, 'adminarea/tickets.html', context)


@user_passes_test(lambda u: u.is_superuser)
def closed_tickets(request):
    tickets = SupportTicket.objects.filter(status='CLOSED').order_by('-timestamp')

    products = Product.objects.all()
        
    context = {
        'tickets':tickets,
        'products':products,
    }
    return render(request, 'adminarea/tickets.html', context)




@user_passes_test(lambda u: u.is_superuser)
def admin_biz_info(request):

    infos = WebsiteInfo.objects.all()

    context = {
        'infos':infos,
        }
    return render(request, 'adminarea/business_info.html', context)



@user_passes_test(lambda u: u.is_superuser)
def biz_info(request, pk):

    info = WebsiteInfo.objects.get(id=pk)
    
    context = {
        'info':info,
        }
    return render(request, 'adminarea/business_info_detail.html', context)



@user_passes_test(lambda u: u.is_superuser)
def admin_reports(request):
    reports = Report.objects.all()
    
    context = {
        'reports':reports,
        }
    return render(request, 'adminarea/all-progress-reports.html', context)


@user_passes_test(lambda u: u.is_superuser)
def report_detail(request, pk):
    report = Report.objects.get(id=pk)
    
    context = {
        'report':report,
        }
    return render(request, 'adminarea/progress-report.html', context)



@user_passes_test(lambda u: u.is_superuser)
def admin_deliverables(request):
    deliverables = Deliverable.objects.all()
    
    context = {
        'deliverables':deliverables,
        }
    return render(request, 'adminarea/all-deliverables.html', context)


@user_passes_test(lambda u: u.is_superuser)
def deliverable_detail(request, pk):
    deliverable = Deliverable.objects.get(id=pk)
    
    context = {
        'deliverable':deliverable,
        }
    return render(request, 'adminarea/deliverable.html', context)



@user_passes_test(lambda u: u.is_superuser)
def admin_billing(request):
    if request.method == "POST":
        cost = request.POST['cost']
        billed_for = request.POST['for']
        user_id = request.POST['user']
        date = request.POST['date']

        user = User.objects.get(id=user_id)

        BillingReceipt.objects.create(
            user=user,
            cost=cost, 
            billed_for=billed_for,
            date=date,
        )

        created = 'true'

        users = User.objects.all()
        
        context = {
            'users':users,
            'created':created,
        }
        return render(request, 'adminarea/billing.html', context)


    users = User.objects.all()
        
    context = {
        'users':users,
    }
    return render(request, 'adminarea/billing.html', context)





########## CRM SECTION #########

class UpdateReferralView(UpdateView):
    model = Referral
    template_name = 'adminarea/update-referral.html'
    form_class = UpdateReferral
    success_url = reverse_lazy('admin-dashboard')



@login_required
def referral_detail(request, pk):

    referral = Referral.objects.get(id=pk)

    context = { 
        'referral':referral,
        }

    return render(request, 'adminarea/referral_detail.html', context)

@login_required
def all_referrals(request):

    referrals = Referral.objects.filter(converted=False).order_by("-id")

    converted_referrals = Referral.objects.filter(converted=True).order_by("-id")

    context = { 
        'converted_referrals':converted_referrals,
        'referrals':referrals,
        }

    return render(request, 'adminarea/all_referrals.html', context)



@login_required
def products(request):
    products = Product.objects.all()
    pf = ProductFilter(request.GET, queryset=products)
    products = pf.qs
    return render(request,'adminarea/products.html',{'products':products,'pf':pf})

@login_required
def delete_product(request, pk):
    product = Product.objects.get(id=pk)
    product.delete()
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def update_product(request, pk):
    product = Product.objects.get(id=pk)
    form = ProductForm(instance=product)
    if request.method == 'POST':
        form = ProductForm(request.POST,instance=product)
        if form.is_valid():
            form.save()
            return redirect('/products')
    context = {'form': form}
    return render(request,'adminarea/form_page.html',context)

@login_required
def create_product(request):
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/support/products')
    context = {'form':form}
    return render(request,'adminarea/form_page.html', context)

@login_required
def orders(request):
    # orders = Order.objects.all()
    orders = Order.objects.order_by("-date_created")
    orders_label = set()
    for o in orders:
        orders_label.add(o.product)
    orders_group = list(Order.objects.values('product').annotate(dcount=Count('product')))
    og = []
    for o in orders_group:
        og.append(o["dcount"])
    total_orders = orders.count()
    recent_orders = orders.order_by('-date_created')[:5]
    context  = {'orders': orders, 'orders_label': orders_label, 'products': products,
    'total_orders':total_orders, 'recent_orders':recent_orders,'og':og}

    return render(request,'adminarea/orders.html', context)

@login_required
def contacts(request):
    req = request.GET.get('search',None)
    if req is not None:
        query = request.GET.get('search')
        customers = Lead.objects.filter(Q(name__icontains=query) | Q(business_name__icontains=query)
        | Q(phone_number__icontains=query)
        | Q(city__icontains=query))
    else:
        customers = Lead.objects.all()
    return render(request,'adminarea/contacts.html',{'customers':customers})

@login_required
def add_contact(request):
    form = CreateLead()
    if request.method == 'POST':
        form = CreateLead(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/contacts')
    context = {'form':form}
    return render(request,"adminarea/form_page.html",context)

@login_required
def update_contact(request, pk):
    contact = Lead.objects.get(id=pk)
    form = UpdateLead(instance=contact)
    if request.method == 'POST':
        form = UpdateLead(request.POST,instance=contact)
        if form.is_valid():
            form.save()
            return redirect('/contacts')
    context = {'form': form}
    return render(request,'adminarea/form_page.html',context)

@login_required
def delete_contact(request, pk):
    contact = Lead.objects.get(id=pk)
    contact.delete()
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def customer_orders(request, pk):
    customer = Lead.objects.get(id=pk)
    order = customer.order_set.all()
    total_orders = order.count()
    context = {'customer':customer,'order':order, 'total_orders':total_orders}
    return render(request,'adminarea/customer_orders.html', context)

@login_required
def create_order(request):
    form = Form()
    if request.method == 'POST':
        form = Form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/support/orders')
    context = {'form':form}
    return render(request,'adminarea/form_page.html', context)

@login_required
def update_order(request, pk):
    order = Order.objects.get(id=pk)
    form = Form(instance=order)
    if request.method == 'POST':
        form = Form(request.POST,instance=order)
        if form.is_valid():
            form.save()
            return redirect('/orders')
    context = {'form': form}
    return render(request,'adminarea/form_page.html',context)
    
@login_required
def delete_order(request, pk):
    order = Order.objects.get(id=pk)
    order.delete()
    return redirect(request.META.get('HTTP_REFERER'))

 
 

##################### TASK MANAGER #####################
def task(request):
    task = Task.objects.all().order_by('-date_created')
    return render(request,'adminarea/task.html',{'task':task})

def add_task(request):
    if request.method == 'POST':
        tname = request.POST.get('task_name')
        tdesc = request.POST.get('task_desc')
        if (tname != ""):
            task = Task.objects.create(name=tname,desc=tdesc)
            task.save()
    return redirect('/task')

def del_task(request,pk):
    task = Task.objects.get(id=pk)
    task.delete()
    return redirect('/support/task')

