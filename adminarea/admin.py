from django.contrib import admin

from .models import *

admin.site.register(BusinessHours)
admin.site.register(FrequentlyAskedQuestion)
admin.site.register(SocialLink)
admin.site.register(WebsiteInfo)
admin.site.register(SupportTicket)
admin.site.register(Support_Ticket_Response)
admin.site.register(BillingReceipt)
admin.site.register(Referral)

 
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'business_name', 'name')

# Lead generation and Admin Dashboard
admin.site.register(Lead, SupportTicketAdmin)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(SalesAgent)

#Task Manager
admin.site.register(Task)

# Website templates
admin.site.register(Template)
admin.site.register(UserTemplate)

# Promos
admin.site.register(Promo)


