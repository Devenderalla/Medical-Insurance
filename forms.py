from django import forms
from .models import *

class Contactforms(forms.ModelForm):
    class Meta:
        model = Contact
        fields = "__all__"


class Customerforms(forms.ModelForm):
    class Meta:
        model = Customer
        exclude = ["cstatus"]


class Vendorforms(forms.ModelForm):
    class Meta:
        model = Vendor
        exclude = ["vstatus"]


class Adminforms(forms.ModelForm):
    class Meta:
        model = Admin
        fields = "__all__"


class PackageForms(forms.ModelForm):
    class Meta:
        model = Package
        fields = "__all__"


class BuyForms(forms.ModelForm):
    class Meta:
        model = Buy
        fields = ["packages", "email", "vemail", "title", "discription", "suminsured", "amount_pay_for_year",
                  "noofyears"]


class UplodfileForms(forms.ModelForm):
    class Meta:
        model = Uplodfile
        fields = "__all__"


class AddfamilyForms(forms.ModelForm):
    class Meta:
        model = Addfamily
        fields = "__all__"


class NotificationForms(forms.ModelForm):
    class Meta:
        model = Notification
        fields = "__all__"


class SubmitclaimForms(forms.ModelForm):
    class Meta:
        model = Submit_Claim
        exclude = ["reasons","sstatus"]


class HospitalsForms(forms.ModelForm):
    class Meta:
        model = Hospitals
        fields = "__all__"

class Admit_RequestsForms(forms.ModelForm):
    class Meta:
        model = Admit_Requests
        exclude = ["bstatus"]
