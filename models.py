from django.db import models
from django.utils import timezone


# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.CharField(max_length=100)


class Customer(models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    age = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    dob = models.DateField()
    phone = models.BigIntegerField()
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    pincode = models.BigIntegerField()
    cprofile = models.FileField()
    cstatus = models.CharField(max_length=100, default="On Hold")


class Vendor(models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    age = models.BigIntegerField()
    gender = models.CharField(max_length=100)
    phone = models.BigIntegerField()
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    pincode = models.BigIntegerField()
    cprofile = models.FileField()
    vstatus = models.CharField(max_length=100, default="On Hold")


class Package(models.Model):
    title = models.CharField(max_length=100)
    discription = models.CharField(max_length=100)
    suminsured = models.FloatField()
    amount_pay_for_year = models.FloatField()
    apply_for = models.CharField(max_length=100)
    corona_ka_watch = models.CharField(max_length=100)
    conditions = models.CharField(max_length=100)
    includes = models.CharField(max_length=100)
    eligibility = models.CharField(max_length=100)
    roomeligibility = models.CharField(max_length=100)
    prebills = models.CharField(max_length=100)
    postbills = models.CharField(max_length=100)
    ambulence = models.CharField(max_length=100)
    excludes = models.CharField(max_length=100)
    ptimestamp = models.DateTimeField(auto_now=True)
    email = models.EmailField()


class Buy(models.Model):
    packages = models.ForeignKey(Package, on_delete=models.CASCADE)
    email = models.EmailField()
    vemail = models.EmailField()
    title = models.CharField(max_length=100)
    discription = models.CharField(max_length=100)
    suminsured = models.FloatField()
    noofyears = models.BigIntegerField()
    amount_pay_for_year = models.FloatField()
    btimestamp = models.DateTimeField(auto_now=True)
    bstatus = models.CharField(max_length=100, default="Pending")


class Uplodfile(models.Model):
    buy = models.ForeignKey(Buy, on_delete=models.CASCADE)
    btimestamp = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=100)
    ufile = models.FileField()


class Addfamily(models.Model):
    fullname = models.CharField(max_length=100)
    email = models.EmailField()
    relation = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    age = models.BigIntegerField()
    dob = models.DateField()


class Notification(models.Model):
    title = models.CharField(max_length=100)
    discription = models.CharField(max_length=100)
    adddate = models.DateTimeField(auto_now=True)


class Hospitals(models.Model):
    email = models.EmailField()
    hospital_name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    contact_number = models.BigIntegerField()
    website = models.CharField(max_length=100)
    services = models.CharField(max_length=100)


class Submit_Claim(models.Model):
    buy_id = models.ForeignKey(Buy, on_delete=models.CASCADE)
    packages = models.BigIntegerField()
    customer_email = models.EmailField()
    vendor_email = models.EmailField()
    hospital_name = models.CharField(max_length=100)
    admit_date = models.DateField()
    discharge_date = models.DateField()
    doctor_name = models.CharField(max_length=100)
    reasonfor_admit = models.CharField(max_length=100)
    discription = models.CharField(max_length=100)
    test_reports = models.FileField()
    discharge_summary = models.FileField()
    final_bill = models.FileField()
    claim_amount = models.BigIntegerField()
    submit_datetime = models.DateTimeField(auto_now=True)
    sstatus = models.CharField(max_length=100,default="Waiting")
    reasons = models.CharField(max_length=1000)


class Admin(models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=100)

    class Meta:
        db_table = "Admin"

class Admit_Requests(models.Model):
    email = models.EmailField()
    vendor_email = models.EmailField()
    hospitals = models.ForeignKey(Hospitals, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    discription = models.CharField(max_length=100)
    hospital_name = models.CharField(max_length=100)
    reasonfor_admit = models.CharField(max_length=100)
    patient_name = models.CharField(max_length=100)
    relationship = models.CharField(max_length=100)
    admit_date = models.DateField()
    booking_date = models.DateTimeField(auto_now=True)
    bstatus = models.CharField(max_length=100,default='Pending')


    class Meta:
        db_table = "Admit_Requests"
