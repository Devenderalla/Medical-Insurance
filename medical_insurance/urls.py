"""medical_insurance URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from medical_insuranceapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),
    path('about', views.about, name="about"),
    path('contact', views.contact, name="contact"),
    path('customer_registraction', views.customer_registraction, name="customer_registraction"),
    path('vendor_registraction', views.vendor_registraction, name="vendor_registraction"),
    path('customer_login', views.customer_login, name= "customer_login"),
    path('customer_home', views.customer_home, name= "customer_home"),
    path('customer_change_password', views.customer_change_password, name="customer_change_password"),
    path('customer_logout', views.customer_logout, name="customer_logout"),
    path('customer_profile', views.customer_profile, name="customer_profile"),
    path('vendor_login', views.vendor_login, name="vendor_login"),
    path('vendor_home', views.vendor_home, name="vendor_home"),
    path('vendor_change_password', views.vendor_change_password, name="vendor_change_password"),
    path('vendor_logout', views.vendor_logout, name="vendor_logout"),
    path('vendor_profile', views.vendor_profile, name="vendor_profile"),
    path('delete_vendor/<int:id>', views.delete_vendor, name="delete_vendor"),
    path('customer_update', views.customer_update, name="customer_update"),
    path('customer_u_update', views.customer_u_update, name="customer_u_update"),
    path('delete_customer/<int:id>', views.delete_customer, name="delete_customer"),
    path('vendor_update', views.vendor_update, name="vendor_update"),
    path('vendor_u_update', views.vendor_u_update, name="vendor_u_update"),
    path('admin_login', views.admin_login, name="admin_login"),
    path('admin_home', views.admin_home, name="admin_home"),
    path('admin_change_password', views.admin_change_password, name="admin_change_password"),
    path('admin_customer', views.admin_customer, name="admin_customer"),

    path('admin_vendors', views.admin_vendors, name="admin_vendors"),
    path('admin_delete_customer/<int:id>', views.admin_delete_customer, name="admin_delete_customer"),

    path('admin_delete_vendors/<int:id>', views.admin_delete_vendors, name="admin_delete_vendors"),
    path('view_contacts', views.view_contacts, name="view_contacts"),
    path('accept_users/<int:id>', views.accept_users, name="accept_users"),
    path('reject_users/<int:id>', views.reject_users, name="reject_users"),
    path('accept_vendors/<int:id>', views.accept_vendors, name="accept_vendors"),
    path('reject_vendors/<int:id>', views.reject_vendors, name="reject_vendors"),
    path('add_packages', views.add_packages, name="add_packages"),

    path('vendor_view_packages', views.vendor_view_packages, name="vendor_view_packages"),
    path('delete_vendor_package/<int:id>', views.delete_vendor_package, name="delete_vendor_package"),
    path('customer_view_packages/<str:email>', views.customer_view_packages, name="customer_view_packages"),
    path('buy_packages/<int:id>', views.buy_packages, name="buy_packages"),
    path('my_packages', views.my_packages, name="my_packages"),
    path('vendor_view_buys', views.vendor_view_buys, name="vendor_view_buys"),

    path('accept_buys/<int:id>', views.accept_buys, name="accept_buys"),
    path('reject_buys/<int:id>', views.reject_buys, name="reject_buys"),

    path('upload_file/<int:id>', views.upload_file, name="upload_file"),
    path('customer_view_files/<int:id>', views.customer_view_files, name="customer_view_files"),
    path('addfamily', views.addfamily, name="addfamily"),
    path('myfamily', views.myfamily, name="myfamily"),
    path('delete_myfamily/<int:id>', views.delete_myfamily, name="delete_myfamily"),
    path('edit_myfamily/<int:id>', views.edit_myfamily, name="edit_myfamily"),
    path('update_myfamily', views.update_myfamily, name="update_myfamily"),
    path('vendor_view_family/<int:id>', views.vendor_view_family, name="vendor_view_family"),
    path('notification', views.notification, name="notification"),
    path('customer_notification', views.customer_notification, name="customer_notification"),
    path('view_notification', views.view_notification, name="view_notification"),
    path('delete_notification/<int:id>', views.delete_notification, name="delete_notification"),
    path('cashless_hospitals', views.cashless_hospitals, name="cashless_hospitals"),
    path('hospitals/<str:email>', views.hospitals, name="hospitals"),
    path('customer_vendors', views.customer_vendors, name="customer_vendors"),
    path('vendor_view_hospital', views.vendor_view_hospital, name="vendor_view_hospital"),
    path('delete_vendor_hospitals/<int:id>', views.delete_vendor_hospitals, name="delete_vendor_hospitals"),
    path('submit_claim/<int:id>', views.submit_claim, name="submit_claim"),
    path('vendor_view_claims/<int:id>', views.vendor_view_claims, name="vendor_view_claims"),

    path('customers_view_claims/<int:id>', views.customers_view_claims, name="customers_view_claims"),
    path('accept_claims/<int:id>', views.accept_claims, name="accept_claims"),
    path('reject_claims/<int:id>', views.reject_claims, name="reject_claims"),

    path('admit_hospital_request/<int:id>', views.admit_hospital_request, name="admit_hospital_request"),
    path('vendor_view_admit_hospital_requests/<int:id>', views.vendor_view_admit_hospital_requests, name="vendor_view_admit_hospital_requests"),
    path('accept_admits_requests/<int:id>', views.accept_admits_requests,
         name="accept_admits_requests"),
    path('reject_admits_requests/<int:id>', views.reject_admits_requests,
         name="reject_admits_requests"),
    path('customers_view_admit_hospital_requests', views.customers_view_admit_hospital_requests, name="customers_view_admit_hospital_requests"),

]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

