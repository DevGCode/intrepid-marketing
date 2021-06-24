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
from .forms import *
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect
from django.db.models import Count, Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.http import HttpResponseRedirect
from django.views import generic
from django.shortcuts import render
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from adminarea.models import *
from website.models import Service


################### GLOBAL #####################


# Promo
current_promo = Promo.objects.filter(current=True)


################### USER DASHBOARD MENU UTILS #####################

def referralCount(request):
    # Gets the users unread, converted referrals
    referrals = Referral.objects.filter(read=False)
    user_referrals = referrals.filter(user=request.user)
    referral_count = user_referrals.count()

    return referral_count


def inboxCount(request):
    # Gets the users unread, inbox
    inbox = Support_Ticket_Response.objects.filter(read=False)
    user_inbox = inbox.filter(user=request.user)
    inbox_count = user_inbox.count()

    return inbox_count


def progressCount(request):
    # Gets the users unread, progress reports
    reports = Report.objects.filter(read=False)
    user_reports = reports.filter(user=request.user)
    progress_count = user_reports.count()

    return progress_count


def deliverableCount(request):
    # Gets the users unread, deliverables
    deliverables = Deliverable.objects.filter(read=False)
    user_deliverables = deliverables.filter(user=request.user)
    deliverable_count = user_deliverables.count()

    return deliverable_count



def billingCount(request):
    # Gets the users unread, billing info
    billing = BillingReceipt.objects.filter(read=False)
    user_billing = billing.filter(user=request.user)
    billing_count = user_billing.count()

    return billing_count





################### USER DASHBOARD #####################



def template_picker(request):
    if request.method == "POST":
        selected_template = request.POST['template_id']

        template = Template.objects.get(id=selected_template)

        UserTemplate.objects.create(
            user=request.user,
            template=template
            )

        created = 'TRUE'

        # Gets the users unread support ticket responses and adds to sidebar
        inbox_count = inboxCount(request)

        # Gets the users unread billing receipts
        billing_count = billingCount(request)

        # Gets the users unread progress reports
        progress_count = progressCount(request)

        # Gets the users unread deliverables
        deliverable_count = deliverableCount(request)

        # Gets the users new, converted referrals
        referral_count = referralCount(request)

        templates = Template.objects.all()

        context = {
            'current_promo':current_promo, # current promo
            'referral_count':referral_count, # unread referrals
            'inbox_count':inbox_count,  # unread messages
            'templates':templates,
            'created':created,
            'billing_count':billing_count, # unread billing
            'progress_count':progress_count, # unread progress reports
            'deliverable_count':deliverable_count, # unread deliverables
        }

        return render(request, 'userarea/template-picker.html', context)

    templates = Template.objects.all()

    # Gets the users unread support ticket responses and adds to sidebar
    inbox_count = inboxCount(request)

    # Gets the users unread billing receipts
    billing_count = billingCount(request)

    # Gets the users unread progress reports
    progress_count = progressCount(request)

    # Gets the users unread deliverables
    deliverable_count = deliverableCount(request)

    # Gets the users new, converted referrals
    referral_count = referralCount(request)

    #new
    responses = Support_Ticket_Response.objects.filter(read=False)


    context = {
        'responses':responses,
        'current_promo':current_promo, # current promo
        'referral_count':referral_count, # unread referrals
        'inbox_count':inbox_count,  # unread messages
        'templates':templates,
        'billing_count':billing_count, # unread billing
        'progress_count':progress_count, # unread progress reports
        'deliverable_count':deliverable_count, # unread deliverables
    }

    return render(request, 'userarea/template-picker.html', context)




def referrals(request):
    # Gets the users unread support ticket responses and adds to sidebar
    inbox_count = inboxCount(request)

    # Gets the users unread billing receipts
    billing_count = billingCount(request)

    # Gets the users unread progress reports
    progress_count = progressCount(request)

    # Gets the users unread deliverables
    deliverable_count = deliverableCount(request)

    # Gets the users new, converted referrals
    referral_count = referralCount(request)

    # Gets the users unread support ticket responses and adds to sidebar
    inbox_count = inboxCount(request)

    user_referrals = Referral.objects.filter(user=request.user)

    referrals = user_referrals.filter(converted=True)

    context = {
        'current_promo':current_promo, # current promo
        'referral_count':referral_count, # unread referrals
        'referrals':referrals,
        'billing_count':billing_count, # unread billing
        'inbox_count':inbox_count,  # unread messages
        'progress_count':progress_count, # unread progress reports
        'deliverable_count':deliverable_count, # unread deliverables
    }

    return render(request, 'userarea/referrals.html', context)



class UpdateWebsiteInfoView(UpdateView):
    model = WebsiteInfo
    template_name = 'user/update-info.html'
    fields = '__all__'
    success_url = reverse_lazy('user-profile')



class UserEditView(generic.UpdateView):
    form_class = EditProfileForm
    template_name = 'user/update-profile.html'
    success_url = reverse_lazy('user-profile')

    def get_object(self):
        return self.request.user


class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('password-changed')



def password_changed(request):
    # This view just lets them know it updated their password, update later

    # Gets the users unread support ticket responses and adds to sidebar
    inbox_count = inboxCount(request)

    # Gets the users unread billing receipts
    billing_count = billingCount(request)

    # Gets the users unread progress reports
    progress_count = progressCount(request)

    # Gets the users unread deliverables
    deliverable_count = deliverableCount(request)

    # Gets the users new, converted referrals
    referral_count = referralCount(request)

    # Get the users website information(s)
    website_info = WebsiteInfo.objects.filter(user=request.user)

    #Send the users info
    user = request.user

    created = 'true'

    context = {
        'current_promo':current_promo, # current promo
        'referral_count':referral_count, # unread referrals
        'created':created,
        'billing_count':billing_count, # unread billing
        'user':user,
        'inbox_count':inbox_count,  # unread messages
        'website_info':website_info,
        'progress_count':progress_count, # unread progress reports
        'deliverable_count':deliverable_count, # unread deliverables
    }

    return render(request, 'userarea/password-changed.html', context)



def update_profile(request):

    # Gets the users unread support ticket responses and adds to sidebar
    inbox_count = inboxCount(request)

    # Gets the users unread billing receipts
    billing_count = billingCount(request)

    # Gets the users unread progress reports
    progress_count = progressCount(request)

    # Gets the users unread deliverables
    deliverable_count = deliverableCount(request)

    # Gets the users new, converted referrals
    referral_count = referralCount(request)


    context = {
        'current_promo':current_promo, # current promo
        'referral_count':referral_count, # unread referrals
        'billing_count':billing_count, # unread billing
        'inbox_count':inbox_count,  # unread messages
        'progress_count':progress_count, # unread progress reports
        'deliverable_count':deliverable_count, # unread deliverables
    }

    return render(request, 'userarea/update-profile.html', context)



def info_detail(request, pk):
    # Gets the users unread support ticket responses and adds to sidebar
    inbox_count = inboxCount(request)

    # Gets the users unread billing receipts
    billing_count = billingCount(request)

    # Gets the users unread progress reports
    progress_count = progressCount(request)

    # Gets the users unread deliverables
    deliverable_count = deliverableCount(request)

    # Gets the users new, converted referrals
    referral_count = referralCount(request)

    # Get the users website information in question
    website_info = WebsiteInfo.objects.get(id=pk)

    context = {
        'current_promo':current_promo, # current promo
        'referral_count':referral_count, # unread referrals
        'billing_count':billing_count, # unread billing
        'inbox_count':inbox_count,  # unread messages
        'website_info':website_info,
        'progress_count':progress_count, # unread progress reports
        'deliverable_count':deliverable_count, # unread deliverables
    }

    return render(request, 'userarea/info.html', context)





def user_profile(request):
    # Gets the users unread support ticket responses and adds to sidebar
    inbox_count = inboxCount(request)

    # Gets the users unread billing receipts
    billing_count = billingCount(request)

    # Gets the users unread progress reports
    progress_count = progressCount(request)

    # Gets the users unread deliverables
    deliverable_count = deliverableCount(request)

    # Gets the users new, converted referrals
    referral_count = referralCount(request)

    # Get the users website information(s)
    website_info = WebsiteInfo.objects.filter(user=request.user)

    #Send the users info
    user = request.user

    context = {
        'current_promo':current_promo, # current promo
        'referral_count':referral_count, # unread referrals
        'billing_count':billing_count, # unread billing
        'user':user,
        'inbox_count':inbox_count,  # unread messages
        'website_info':website_info,
        'progress_count':progress_count, # unread progress reports
        'deliverable_count':deliverable_count, # unread deliverables
    }

    return render(request, 'userarea/profile.html', context)



def user_billing(request):
    # Gets the users unread support ticket responses and adds to sidebar
    inbox_count = inboxCount(request)

    # Gets the users unread billing receipts
    billing_count = billingCount(request)

    # Gets the users unread progress reports
    progress_count = progressCount(request)

    # Gets the users unread deliverables
    deliverable_count = deliverableCount(request)

    # Gets the users new, converted referrals
    referral_count = referralCount(request)

    billing = BillingReceipt.objects.filter(user=request.user)

    context = {
        'current_promo':current_promo, # current promo
        'referral_count':referral_count, # unread referrals
        'billing_count':billing_count, # unread billing
        'inbox_count':inbox_count,  # unread messages
        'billing':billing,
        'progress_count':progress_count, # unread progress reports
        'deliverable_count':deliverable_count, # unread deliverables
    }

    return render(request, 'userarea/billing.html', context)



def user_reports(request):
    # Gets the users unread support ticket responses and adds to sidebar
    inbox_count = inboxCount(request)

    # Gets the users unread billing receipts
    billing_count = billingCount(request)

    # Gets the users unread progress reports
    progress_count = progressCount(request)

    # Gets the users unread deliverables
    deliverable_count = deliverableCount(request)

    # Gets the users new, converted referrals
    referral_count = referralCount(request)

    # Get the users reports
    reports = Report.objects.filter(user=request.user)

    context = {
        'reports':reports,
        'current_promo':current_promo, # current promo
        'referral_count':referral_count, # unread referrals
        'inbox_count':inbox_count,  # unread messages
        'billing_count':billing_count, # unread billing
        'progress_count':progress_count, # unread progress reports
        'deliverable_count':deliverable_count, # unread deliverables
    }

    return render(request, 'userarea/reports.html', context)



def deliverables(request):
    # Gets the users unread support ticket responses and adds to sidebar
    inbox_count = inboxCount(request)

    # Gets the users unread billing receipts
    billing_count = billingCount(request)

    # Gets the users unread progress reports
    progress_count = progressCount(request)

    # Gets the users unread deliverables
    deliverable_count = deliverableCount(request)

    # Gets the users new, converted referrals
    referral_count = referralCount(request)

    # Get the users deliverables
    deliverables = Deliverable.objects.filter(user=request.user)

    context = {
        'deliverables':deliverables,
        'current_promo':current_promo, # current promo
        'referral_count':referral_count, # unread referrals
        'inbox_count':inbox_count,  # unread messages
        'billing_count':billing_count, # unread billing
        'progress_count':progress_count, # unread progress reports
        'deliverable_count':deliverable_count, # unread deliverables
    }

    return render(request, 'userarea/deliverables.html', context)



def user_support(request):

    if request.method == "POST":
        subject = request.POST['summary']
        phone_pre = request.POST['phone']
        description = request.POST['body']

        phone_number = '+1' + phone_pre

        SupportTicket.objects.create(
            user=request.user,
            subject=subject,
            phone_number=phone_number,
            description=description
            )

        created = 'TRUE'

        # Gets the users unread support ticket responses and adds to sidebar
        inbox_count = inboxCount(request)

        # Gets the users unread billing receipts
        billing_count = billingCount(request)

        # Gets the users unread progress reports
        progress_count = progressCount(request)

        # Gets the users unread deliverables
        deliverable_count = deliverableCount(request)

        # Gets the users new, converted referrals
        referral_count = referralCount(request)

        tickets = SupportTicket.objects.filter(user=request.user)

        context = {
            'current_promo':current_promo, # current promo
            'referral_count':referral_count, # unread referrals
            'inbox_count':inbox_count,  # unread messages
            'tickets':tickets,
            'created':created,
            'billing_count':billing_count, # unread billing
            'progress_count':progress_count, # unread progress reports
            'deliverable_count':deliverable_count, # unread deliverables
        }

        return render(request, 'userarea/support.html', context)

    all_tickets = SupportTicket.objects.filter(user=request.user)

    tickets = all_tickets.order_by('-timestamp')

    # Gets the users unread support ticket responses and adds to sidebar
    inbox_count = inboxCount(request)

    # Gets the users unread billing receipts
    billing_count = billingCount(request)

    # Gets the users unread progress reports
    progress_count = progressCount(request)

    # Gets the users unread deliverables
    deliverable_count = deliverableCount(request)

    # Gets the users new, converted referrals
    referral_count = referralCount(request)

    #new
    responses = Support_Ticket_Response.objects.filter(read=False)


    context = {
        'responses':responses,
        'current_promo':current_promo, # current promo
        'referral_count':referral_count, # unread referrals
        'inbox_count':inbox_count,  # unread messages
        'tickets':tickets,
        'billing_count':billing_count, # unread billing
        'progress_count':progress_count, # unread progress reports
        'deliverable_count':deliverable_count, # unread deliverables
    }

    return render(request, 'userarea/support.html', context)


def ticket(request, pk):
    # Gets the users unread support ticket responses and adds to sidebar
    inbox_count = inboxCount(request)

    # Gets the users unread billing receipts
    billing_count = billingCount(request)

    # Gets the users unread progress reports
    progress_count = progressCount(request)

    # Gets the users unread deliverables
    deliverable_count = deliverableCount(request)

    # Gets the users new, converted referrals
    referral_count = referralCount(request)

    # Retreive the ticket in question
    ticket = SupportTicket.objects.get(id=pk)

    # Get the responses to that particular ticket
    responses = Support_Ticket_Response.objects.filter(ticket=ticket)

    context = {
        'current_promo':current_promo, # current promo
        'referral_count':referral_count, # unread referrals
        'inbox_count':inbox_count,  # unread messages
        'responses':responses,
        'ticket':ticket,
        'billing_count':billing_count, # unread billing
        'progress_count':progress_count, # unread progress reports
        'deliverable_count':deliverable_count, # unread deliverables
    }

    return render(request, 'userarea/ticket.html', context)





################### WESITE REFERRAL #####################

def referral(request, pk):
    if request.method == "POST":

        message_name = request.POST['name']
        message_url = request.POST['url']
        phone = request.POST['phone']
        date = request.POST['date']

        user = User.objects.get(id=pk)

        Referral.objects.create(
            user=user,
            name=message_name,
            phone=phone,
            call_date=date,
            )

        return render(request, 'referral.html', { 'message_name':message_name })


    user = User.objects.get(id=pk)

    nav_services = Service.objects.all()

    context = {
        'current_promo':current_promo, # current promo
        'user':user,
        'nav_services':nav_services,

    }
    return render(request, 'referral.html', context)




def read_referral(request, pk):
    # Get the referral in question and mark it as read
    referral = Referral.objects.get(id=pk)
    referral.read = True
    referral.save()

    user_referrals = Referral.objects.filter(user=request.user)

    referrals = user_referrals.filter(converted=True)

    # Gets the users unread support ticket responses and adds to sidebar
    inbox_count = inboxCount(request)

    # Gets the users unread billing receipts
    billing_count = billingCount(request)

    # Gets the users unread progress reports
    progress_count = progressCount(request)

    # Gets the users unread deliverables
    deliverable_count = deliverableCount(request)

    # Gets the users new, converted referrals
    referral_count = referralCount(request)

    context = {
        'current_promo':current_promo, # current promo
        'referral':referral,
        'referral_count':referral_count, # unread referrals
        'inbox_count':inbox_count,  # unread messages
        'referrals':referrals,
        'billing_count':billing_count, # unread billing
        'progress_count':progress_count, # unread progress reports
        'deliverable_count':deliverable_count, # unread deliverables
    }

    return render(request, 'userarea/referrals.html', context)



def read_report(request, pk):
    # Get the referral in question and mark it as read
    report = Report.objects.get(id=pk)
    report.read = True
    report.save()

    # Gets the users unread support ticket responses and adds to sidebar
    inbox_count = inboxCount(request)

    # Gets the users unread billing receipts
    billing_count = billingCount(request)

    # Gets the users unread progress reports
    progress_count = progressCount(request)

    # Gets the users unread deliverables
    deliverable_count = deliverableCount(request)

    # Gets the users new, converted referrals
    referral_count = referralCount(request)

    # Get the users reports
    reports = Report.objects.filter(user=request.user)

    context = {
        'reports':reports,
        'current_promo':current_promo, # current promo
        # 'referral':referral,
        'referral_count':referral_count, # unread referrals
        'inbox_count':inbox_count,  # unread messages
        'referrals':referrals,
        'billing_count':billing_count, # unread billing
        'progress_count':progress_count, # unread progress reports
        'deliverable_count':deliverable_count, # unread deliverables
    }

    return render(request, 'userarea/reports.html', context)



def read_deliverable(request, pk):
    # Get the referral in question and mark it as read
    deliverable = Deliverable.objects.get(id=pk)
    deliverable.read = True
    deliverable.save()

    # Gets the users unread support ticket responses and adds to sidebar
    inbox_count = inboxCount(request)

    # Gets the users unread billing receipts
    billing_count = billingCount(request)

    # Gets the users unread progress reports
    progress_count = progressCount(request)

    # Gets the users unread deliverables
    deliverable_count = deliverableCount(request)

    # Gets the users new, converted referrals
    referral_count = referralCount(request)

    # Get the users deliverables
    deliverables = Deliverable.objects.filter(user=request.user)

    context = {
        'deliverables':deliverables,
        'current_promo':current_promo, # current promo
        # 'referral':referral,
        'referral_count':referral_count, # unread referrals
        'inbox_count':inbox_count,  # unread messages
        'referrals':referrals,
        'billing_count':billing_count, # unread billing
        'progress_count':progress_count, # unread progress reports
        'deliverable_count':deliverable_count, # unread deliverables
    }

    return render(request, 'userarea/deliverables.html', context)



def read_ticket(request, pk):
    # Get the ticket response in question and mark it as read
    ticket_response = Support_Ticket_Response.objects.get(id=pk)
    ticket_response.read = True
    ticket_response.save()
    tickets = SupportTicket.objects.filter(user=request.user)

    # Gets the users unread support ticket responses and adds to sidebar
    inbox_count = inboxCount(request)

    # Gets the users unread billing receipts
    billing_count = billingCount(request)

    # Gets the users unread progress reports
    progress_count = progressCount(request)

    # Gets the users unread deliverables
    deliverable_count = deliverableCount(request)

    # Gets the users new, converted referrals
    referral_count = referralCount(request)

    context = {
        'current_promo':current_promo, # current promo
        'referral_count':referral_count, # unread referrals
        'inbox_count':inbox_count,  # unread messages
        'tickets':tickets,
        'billing_count':billing_count, # unread billing
        'progress_count':progress_count, # unread progress reports
        'deliverable_count':deliverable_count, # unread deliverables
    }

    return render(request, 'userarea/support.html', context)



def read_billing(request, pk):
    # Get the billing receipt in question and mark it as read
    billing = BillingReceipt.objects.get(id=pk)
    billing.read = True
    billing.save()

    # Gets the users unread support ticket responses and adds to sidebar
    inbox_count = inboxCount(request)

    # Gets the users unread billing receipts
    billing_count = billingCount(request)

    # Gets the users unread progress reports
    progress_count = progressCount(request)

    # Gets the users unread deliverables
    deliverable_count = deliverableCount(request)

    # Gets the users new, converted referrals
    referral_count = referralCount(request)

    billing = BillingReceipt.objects.filter(user=request.user)

    context = {
        'current_promo':current_promo, # current promo
        'referral_count':referral_count, # unread referrals
        'billing':billing,
        'inbox_count':inbox_count,  # unread messages
        # 'tickets':tickets,
        'billing_count':billing_count, # unread billing
        'progress_count':progress_count, # unread progress reports
        'deliverable_count':deliverable_count, # unread deliverables
    }

    return render(request, 'userarea/billing.html', context)




def add_ticket_response(request, pk):
    if request.method == "POST":
        subject = request.POST['summary']
        description = request.POST['body']

        ticket = SupportTicket.objects.get(id=pk)

        Support_Ticket_Response.objects.create(
            user=request.user,
            ticket=ticket,
            subject=subject,
            description=description
            )

        created = 'TRUE'

        # Gets the users unread support ticket responses and adds to sidebar
        inbox_count = inboxCount(request)

            # Gets the users unread billing receipts
        billing_count = billingCount(request)

        # Gets the users unread progress reports
        progress_count = progressCount(request)

        # Gets the users unread deliverables
        deliverable_count = deliverableCount(request)

        # Gets the users new, converted referrals
        referral_count = referralCount(request)

        context = {
            'current_promo':current_promo, # current promo
            'referral_count':referral_count, # unread referrals
            'inbox_count':inbox_count,  # unread messages
            'created':created,
            'ticket':ticket,
            'billing_count':billing_count, # unread billing
            'progress_count':progress_count, # unread progress reports
            'deliverable_count':deliverable_count, # unread deliverables
            }

        return render(request, 'userarea/ticket-response.html', context)

    ticket = SupportTicket.objects.get(id=pk)

    # Gets the users unread support ticket responses and adds to sidebar
    inbox_count = inboxCount(request)

    # Gets the users unread billing receipts
    billing_count = billingCount(request)

    # Gets the users unread progress reports
    progress_count = progressCount(request)

    # Gets the users unread deliverables
    deliverable_count = deliverableCount(request)

    # Gets the users new, converted referrals
    referral_count = referralCount(request)

    context = {
            'current_promo':current_promo, # current promo
            'referral_count':referral_count, # unread referrals
            'inbox_count':inbox_count,  # unread messages
            'ticket':ticket,
            'billing_count':billing_count, # unread billing
            'progress_count':progress_count, # unread progress reports
            'deliverable_count':deliverable_count, # unread deliverables
        }

    return render(request, 'userarea/ticket-response.html', context)
