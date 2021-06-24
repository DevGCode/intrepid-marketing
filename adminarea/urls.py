from .views import *
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views

urlpatterns = [
    # tasks
    path('task/', task, name="task"),
    path('add-task/', add_task, name="add_task"),
    path('del-task/<str:pk>', del_task, name="del_task"),
    # CRM
    path('admin-dashboard/', support_dashboard, name="admin-dashboard"),
    path('update-lead/<int:pk>/', UpdateLeadView.as_view(), name="update-lead"),
    path('products/', products, name="products"),
    path('create-product/', create_product, name="create_product"),
    path('update-product/<str:pk>/', update_product, name="update_product"),
    path('delete-product/<str:pk>/', delete_product, name="delete_product"),
    path('orders/', orders, name="orders"),
    path('contacts/', contacts, name="contacts"),
    path('delete-contact/<str:pk>/', delete_contact, name="delete_contact"),
    path('update-contact/<str:pk>/', update_contact, name="update_contact"),
    path('add-contact/', add_contact, name="add_contact"),
    path('customer-orders/<str:pk>/', customer_orders, name="customer_orders"),
    path('create-order/', create_order, name="create_order"),
    path('update-order/<str:pk>', update_order, name="update_order"),
    path('delete-order/<str:pk>', delete_order, name="delete_order"),
    # remove from call list
    path('remove/<int:pk>', remove_from_list, name="remove"),
    # add as client
    path('add/<int:pk>', add_as_client, name="add"),
    path('create-response/<int:pk>', create_response, name="create-response"),
    # get weather
    path('get-weather/', get_weather, name="get-weather"),
    # reports
    path('reports/', reports, name="reports"),
    path('toggle_product/<int:cats>/', toggle_product, name="toggle_product"),
    path('website_leads', website_leads, name="website_leads"),
    path('client_leads', client_leads, name="client_leads"),
    path('create-lead/', CreateLeadView.as_view(), name="create_lead"),
    # support tickets
    path('tickets', tickets, name="tickets"),
    path('paused', paused_tickets, name="paused"),
    path('closed', closed_tickets, name="closed"),
    # billing
    path('admin-billing', admin_billing, name="admin-billing"),
    # business info
    path('admin-biz-info', admin_biz_info, name="admin-biz-info"),
    path('biz-info/<int:pk>/', biz_info, name="biz-info"),
    path('admin-reports/', admin_reports, name="admin-reports"),
    path('report-detail/<int:pk>', report_detail, name="report-detail"),
    path('admin-deliverables/', admin_deliverables, name="admin-deliverables"),
    path('deliverable-detail/<int:pk>', deliverable_detail, name="deliverable-detail"),
    # referrals
    path('referral-detail/<int:pk>', referral_detail, name="referral-detail"),
    path('all-referrals', all_referrals, name="all-referrals"),
    path('update-referral/<int:pk>', UpdateReferralView.as_view(), name="update-referral"),

]
