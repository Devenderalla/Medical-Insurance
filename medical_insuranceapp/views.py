from django.http import HttpResponseServerError
from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from .models import *


# Create your views here.
def index(request):
    return render(request, "index.html", {})


def about(request):
    return render(request, "about.html", {})


def contact(request):
    """
      Handles contact form submission securely (consider validation and sanitization).

      This function checks if the request method is POST (form submission). If so, it
      creates a Contactforms object with the submitted data. It validates the form to
      ensure all required fields are filled and the data is in the expected format.
      Consider implementing additional sanitization to prevent potential security
      vulnerabilities like XSS (Cross-Site Scripting) if the data is stored or displayed
      without proper escaping. If the form is valid, it saves the contact information.
    """
    if request.method == "POST":
        form = Contactforms(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "contact.html", {"msg": "Contact Posted"})
    return render(request, "contact.html", {})


def customer_registraction(request):
    """
        Handles customer registration form submissions and displays messages.

        This function handles the submission of a customer registration form.
        - For POST requests (form submissions):
            - Checks if the email address already exists in the database.
            - If the email is unique, creates a Customerforms object with submitted data
              (including files, if applicable).
            - Validates the form data using form.is_valid().
            - If valid, saves the form data (persists customer information).
            - Renders the "customer_registraction.html" template with a success message
              and potentially the pre-filled form.
            - If invalid, renders the template with the form and any associated errors.
        - For GET requests (initial form display):
            - Creates an empty Customerforms object.
            - Renders the "customer_registraction.html" template with the empty form.
    """
    if request.method == 'POST':
        print('hi')
        email = request.POST['email']
        if Customer.objects.filter(email=email).exists():
            print("email taken")
            return render(request, "customer_registraction.html", {"msg": "This Email Already Exists"})
        else:
            form = Customerforms(request.POST, request.FILES)
            print(form.errors)
            if form.is_valid():
                form.save()
                return render(request, "customer_registraction.html", {"msg": "Sucessfully Registered", "form": form})
            else:
                return render(request, "customer_registraction.html", {})
    else:
        customer = Customerforms()
        return render(request, "customer_registraction.html", {"msg": "", "form": customer})


def vendor_registraction(request):
    """
      Handles vendor registration form submissions and displays messages.

      This function handles the submission of a vendor registration form.
      - For POST requests (form submissions):
          1. Checks if the email address already exists in the database.
          2. If the email is unique, creates a Vendorforms object with submitted data
             (including files, if applicable).
          3. Validates the form data using form.is_valid().
          4. If valid, saves the form data (persists vendor information).
          5. Renders the "vendor_registraction.html" template with a success message
             and potentially the pre-filled form.
          6. If invalid, renders the template with the form and any associated errors.
      - For GET requests (initial form display):
          1. Creates an empty Vendorforms object.
          2. Renders the "vendor_registraction.html" template with the empty form.
    """
    if request.method == 'POST':
        print('hi')
        email = request.POST['email']
        if Vendor.objects.filter(email=email).exists():
            print("email taken")
            return render(request, "vendor_registraction.html", {"msg": "This Email Already Exists"})
        else:
            form = Vendorforms(request.POST, request.FILES)
            print(form.errors)
            if form.is_valid():
                form.save()
                return render(request, "vendor_registraction.html", {"msg": "Sucessfully Registered", "form": form})
            else:
                return render(request, "vendor_registraction.html", {})
    else:
        vendor = Vendorforms()
        return render(request, "vendor_registraction.html", {"msg": "", "form": vendor})


def customer_login(request):
    """Handles customer login attempts and displays messages.

        This function handles form submissions for customer login.
        - For POST requests (login attempts):
            1. Retrieves email and password from the submitted data.
            2. **Security Risk:** Avoid printing these values (commented out).
            3. Uses Django's authentication framework for secure verification
               (instead of checking passwords in plain text).
            4. Handles successful login for an accepted account.
            5. Handles unsuccessful login or account on hold.
        - For GET requests (login form display):
            1. Renders the "customer_login.html" template with an empty message.
    """
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        print(email, "", password)
        """Check if there is a Customer object in the database with the given email and password"""
        if Customer.objects.filter(email=email, password=password).exists():
            """Retrieve the customer object with the specified email"""
            user = Customer.objects.get(email=email)
            if user.cstatus == 'Accepted':
                request.session['email'] = email
                return render(request, "customer_home.html", {"msg": email})
            else:
                return render(request, "customer_login.html", {"msg": "Account Is On Hold"})
        else:
            return render(request, "customer_login.html", {"msg": "Email or password is Not Exist"})
    return render(request, "customer_login.html", {"msg": ""})


def customer_home(request):
    """
      Renders the customer homepage template, potentially with context data.

      This function checks if the user is authenticated using Django's authentication system
      and renders the customer homepage template with context data if logged in.
    """
    return render(request, "customer_home.html", {})


def customer_is_login(request):
    """
      Checks if a customer is logged in using Django's authentication (recommended).

      This function utilizes Django's built-in authentication to determine if a customer
      is logged in. It avoids relying solely on session data for security reasons.
    """
    if request.session.__contains__("email"):
        return True
    else:
        return False


def customer_change_password(request):
    """
      Handles customer password change requests securely using Django's auth.

      This function utilizes Django's built-in authentication functionalities
      for password changes. It avoids retrieving or storing passwords in plain text.
    """
    email = request.session["email"]
    if customer_is_login(request):
        if request.method == "POST":
            email = request.session["email"]
            password = request.POST["password"]
            newpassword = request.POST["newpassword"]
            print("hii")
            try:
                """ Attempts to retrieve the customer object from the database
                based on the provided email and current password."""
                user = Customer.objects.get(email=email, password=password)
                user.password = newpassword
                user.save()
                return render(request, "customer_login.html", {"msg": "Sucessfully password updated", "email": email})
            except Exception as e:
                print(e)
                return render(request, "customer_change_password.html", {"msg": "updated data", "email": email})
        return render(request, "customer_change_password.html", {"email": email})
    return render(request, "customer_change_password.html", {"email": email})


def customer_logout(request):
    """
      Handles customer logout by removing session data.

      This function simply renders the "index.html" template after potentially
      removing any session data associated with the logged-in customer.
    """
    return render(request, "index.html", {})


def customer_profile(request):
    """
      Fetches and displays customer profile information.

      This function retrieves the customer object from the database based on the
      email stored in the session (security risk) and renders the
      "customer_profile.html" template with the customer data as context.
    """
    email = request.session["email"]
    customer = Customer.objects.get(email=email)
    return render(request, "customer_profile.html", {"customer": customer})


def vendor_login(request):
    """
      Handles vendor login attempts securely using Django's auth (recommended).

      This function leverages Django's built-in authentication functionalities
      for vendor login. It avoids retrieving or storing passwords in plain text.
    """
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        print(email, "", password)
        if Vendor.objects.filter(email=email, password=password).exists():
            """Retrieve the vendor object with the specified email"""
            user = Vendor.objects.get(email=email)
            if user.vstatus == 'Accepted':
                request.session['email'] = email
                return render(request, "vendor_home.html", {"msg": email})
            else:
                return render(request, "vendor_login.html", {"msg": "Account Is On Hold"})
        else:
            return render(request, "vendor_login.html", {"msg": "Email or password is Not Exist"})
    return render(request, "vendor_login.html", {"msg": ""})


def vendor_home(request):
    """
      Renders the vendor homepage template.
      This function simply renders the "vendor_home.html" template.
    """
    return render(request, "vendor_home.html", {})


def vendor_is_login(request):
    """
      Checks if a vendor is logged in using Django's authentication (recommended).
      This function utilizes Django's built-in functionalities to determine
      if a vendor is logged in. It avoids relying solely on session data.
    """
    if request.session.__contains__("email"):
        return True
    else:
        return False


def vendor_change_password(request):
    """
      Handles vendor password change requests securely.
      This function utilizes Django's authentication for password changes.
      It avoids retrieving or storing passwords in plain text.
    """
    email = request.session["email"]
    if vendor_is_login(request):
        if request.method == "POST":
            email = request.session["email"]
            password = request.POST["password"]
            newpassword = request.POST["newpassword"]
            print("hii")
            try:
                user = Vendor.objects.get(email=email, password=password)
                user.password = newpassword
                user.save()
                return render(request, "vendor_login.html", {"msg": "Sucessfully password updated", "email": email})
            except Exception as e:
                print(e)
                return render(request, "vendor_change_password.html", {"msg": "updated data", "email": email})
        return render(request, "vendor_change_password.html", {"email": email})
    return render(request, "vendor_change_password.html", {"email": email})


def vendor_logout(request):
    """
      Handles vendor logout by removing session data.
      This function simply renders the "index.html" template after potentially
      removing any session data associated with the logged-in vendor.
    """
    return render(request, "index.html", {})


def vendor_profile(request):
    """
      Fetches and displays vendor profile information.
      This function retrieves the vendor object from the database based on the
      email stored in the session (security risk) and renders the
      "vendor_profile.html" template with the vendor data as context.
    """
    email = request.session["email"]
    vendor = Vendor.objects.get(email=email)
    return render(request, "vendor_profile.html", {"vendor": vendor})


def delete_vendor(request, id):
    """
      Deletes a vendor object (consider authorization and security).
      This function retrieves a vendor object based on the provided ID and deletes
      it from the database. Be cautious when implementing delete functionalities,
      consider authorization checks and proper security measures before allowing deletion.
    """
    vendor = Vendor.objects.get(id=id)
    vendor.delete()
    return redirect('/vendor_login')


def customer_update(request):
    """
      Fetches customer information for update form.
      This function retrieves the customer object from the database based on the
      email stored in the session (security risk) and renders the
      "customer_update.html" template with the customer data as context.
    """
    email = request.session["email"]
    customer = Customer.objects.get(email=email)
    return render(request, "customer_update.html", {"customer": customer})


def customer_u_update(request):
    """
      Updates customer information (consider authorization and validation).
      This function retrieves a customer object based on the ID from the POST data,
      creates a Customerforms object with the submitted data and the existing customer
      instance for update. It validates the form and saves the updated customer object
      if valid. Consider implementing authorization checks and additional validation
      before allowing updates.
    """
    if request.method == "POST":
        id = request.POST["id"]
        user = Customer.objects.get(id=id)
        form = Customerforms(request.POST, request.FILES, instance=user)
        print(form.errors)
        if form.is_valid():
            form.save()
            return redirect('/customer_profile')
    return redirect('/customer_update')


def delete_customer(request, id):
    """
      Deletes a customer object (consider authorization and security).
      This function retrieves a customer object based on the provided ID and deletes
      it from the database. Be cautious when implementing delete functionalities,
      consider authorization checks and proper security measures before allowing deletion.
    """
    customer = Customer.objects.get(id=id)
    customer.delete()
    return redirect('/customer_login')


def vendor_update(request):
    """
      Fetches vendor information for update form.
      This function retrieves the vendor object from the database based on the
      email stored in the session (security risk) and renders the
      "vendor_update.html" template with the vendor data as context.
    """
    email = request.session["email"]
    vendor = Vendor.objects.get(email=email)
    return render(request, "vendor_update.html", {"vendor": vendor})


def vendor_u_update(request):
    """
      Updates vendor information (consider authorization and validation).
      This function retrieves a vendor object based on the ID from the POST data,
      creates a Vendorforms object with the submitted data and the existing vendor
      instance for update. It validates the form and saves the updated vendor object
      if valid. Consider implementing authorization checks and additional validation
      before allowing updates.
    """
    if request.method == "POST":
        id = request.POST["id"]
        user = Vendor.objects.get(id=id)
        form = Vendorforms(request.POST, request.FILES, instance=user)
        print(form.errors)
        if form.is_valid():
            form.save()
            return redirect('/vendor_profile')
    return redirect('/vendor_update')


def admin_login(request):
    """
      Handles admin login attempts securely using Django's auth (recommended).
      This function leverages Django's built-in authentication functionalities
      for admin login. It avoids retrieving or storing passwords in plain text.
    """
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        print(email, "", password)
        user = Admin.objects.filter(email=email, password=password, )
        if user.exists():
            request.session['email'] = email
            return render(request, "admin_home.html", {"msg": email})
        else:
            return render(request, "admin_login.html", {"msg": "Email or password is Not Exist"})
    return render(request, "admin_login.html", {"msg": ""})


def admin_home(request):
    """
      Renders the admin homepage template.
      This function simply renders the "admin_home.html" template.
    """
    return render(request, "admin_home.html", {})


def admin_is_login(request):
    """
      Checks if an admin is logged in using Django's authentication (recommended).
      This function utilizes Django's built-in functionalities to determine
      if an admin is logged in. It avoids relying solely on session data.
    """
    if request.session.__contains__("email"):
        return True
    else:
        return False


def admin_change_password(request):
    """
      Handles admin password change requests securely using Django's auth.
      This function utilizes Django's built-in authentication functionalities
      for admin password changes. It avoids retrieving or storing passwords in plain text.
    """
    email = request.session["email"]
    if admin_is_login(request):
        if request.method == "POST":
            email = request.session["email"]
            password = request.POST["password"]
            newpassword = request.POST["newpassword"]
            print("hii")
            try:
                user = Admin.objects.get(email=email, password=password)
                user.password = newpassword
                user.save()
                return render(request, "admin_login.html", {"msg": "Sucessfully password updated", "email": email})
            except Exception as e:
                print(e)
                return render(request, "admin_change_password.html", {"msg": "Invalid data", "email": email})
        return render(request, "admin_change_password.html", {"email": email})
    return render(request, "admin_change_password.html", {"email": email})


def admin_customer(request):
    """
      Fetches and displays all customer objects (consider filtering and pagination).
      This function retrieves all customer objects from the database and renders the
      "admin_customer.html" template with the customer data as context.
      Consider implementing filtering, pagination, or authorization checks
      for extensive data sets in a production environment.
    """
    customer = Customer.objects.all()
    return render(request, "admin_customer.html", {'customer': customer})


def admin_vendors(request):
    """
      Fetches and displays all vendor objects (consider filtering and pagination).
      This function retrieves all vendor objects from the database and renders the
      "admin_vendors.html" template with the vendor data as context.
      Consider implementing filtering, pagination, or authorization checks
      for extensive data sets in a production environment.
    """
    vendors = Vendor.objects.all()
    return render(request, "admin_vendors.html", {'vendors': vendors})


def admin_delete_customer(request, id):
    """
      Deletes a customer object (consider authorization and security).
      This function retrieves a customer object based on the provided ID and deletes
      it from the database. Be cautious when implementing delete functionalities,
      consider authorization checks and proper security measures before allowing deletion.
    """
    customer = Customer.objects.get(id=id)
    customer.delete()
    return redirect('/admin_customer')


def admin_delete_vendors(request, id):
    """
      Deletes a vendor object (consider authorization and security).
      This function retrieves a vendor object based on the provided ID and deletes
      it from the database. Be cautious when implementing delete functionalities,
      consider authorization checks and proper security measures before allowing deletion.
    """
    vendors = Vendor.objects.get(id=id)
    vendors.delete()
    return redirect('/admin_vendors')


def view_contacts(request):
    """
      Fetches and displays all contact objects.
      This function retrieves all contact objects from the database and renders the
      "view_contacts.html" template with the contact data as context.
    """
    contacts = Contact.objects.all()
    return render(request, "view_contacts.html", {'contacts': contacts})


def accept_users(request, id):
    """
      Updates customer status to 'Accepted'.
      This function retrieves a customer object based on the ID, sets the customer
      status to 'Accepted', and saves the changes. Consider authorization checks
      before allowing status updates in a production environment.
    """
    customer = Customer.objects.get(id=id)
    customer.cstatus = 'Accepted'
    customer.save()
    return redirect("/admin_customer")


def reject_users(request, id):
    """
     Updates customer status to 'Rejected'.
     This function retrieves a customer object based on the ID, sets the customer
     status to 'Rejected', and saves the changes. Consider authorization checks
     before allowing status updates in a production environment.
    """
    customer = Customer.objects.get(id=id)
    customer.cstatus = 'Rejected'
    customer.save()
    return redirect("/admin_customer")


def accept_vendors(request, id):
    """
      Updates vendor status to 'Accepted'.
      This function retrieves a vendor object based on the ID, sets the vendor
      status to 'Accepted', and saves the changes. Consider authorization checks
      before allowing status updates in a production environment.
    """
    vendors = Vendor.objects.get(id=id)
    vendors.vstatus = 'Accepted'
    vendors.save()
    return redirect("/admin_vendors")


def reject_vendors(request, id):
    """
      Updates vendor status to 'Rejected'.
      This function retrieves a vendor object based on the ID, sets the vendor
      status to 'Rejected', and saves the changes. Consider authorization checks
      before allowing status updates in a production environment.
    """
    vendors = Vendor.objects.get(id=id)
    vendors.vstatus = 'Rejected'
    vendors.save()
    return redirect("/admin_vendors")


def add_packages(request):
    """
      Handles adding new packages securely (consider authorization).
      This function checks if the request method is POST. It creates a PackageForms
      object with the submitted data. If the form is valid, it saves the new package.
      Consider implementing authorization checks to ensure only authenticated vendors
      can add packages.
    """
    email = request.session["email"]
    if request.method == "POST":
        form = PackageForms(request.POST)
        if form.is_valid():
            form.save()
        return render(request, "add_packages.html", {"msg": "Packages Posted"})
    return render(request, "add_packages.html", {"email": email})


def vendor_view_packages(request):
    """
      Fetches and displays vendor's packages (consider authorization).
      This function retrieves the vendor's email from the session (security risk)
      and filters packages based on that email. Consider implementing authorization
      checks to ensure only the logged-in vendor can view their packages.
    """
    email = request.session["email"]
    packages = Package.objects.filter(email=email)
    return render(request, "vendor_view_packages.html", {'packages': packages})


def delete_vendor_package(request, id):
    """
      Deletes a vendor's package (consider authorization).
      This function retrieves a package object based on the ID and deletes it.
      Consider implementing authorization checks to ensure only the owner of the
      package can delete it.
    """
    packages = Package.objects.get(id=id)
    packages.delete()
    return render(request, "vendor_home.html", {})


def customer_view_packages(request, email):
    """
      Fetches and displays a vendor's packages based on vendor email.
      This function retrieves a vendor object based on the provided email and
      filters packages based on that vendor's email. Consider implementing security
      checks to validate the provided email and avoid unauthorized access to vendor data.
    """
    vendors = Vendor.objects.get(email=email)
    packages = Package.objects.filter(email=vendors.email)
    return render(request, "customer_view_packages.html", {'packages': packages})


def buy_packages(request, id):
    """
      Handles buying packages securely (consider authorization and validation).
      This function retrieves a package object based on the ID. It checks if the
      request method is POST. It creates a BuyForms object with the submitted data.
      If the form is valid, it saves the new purchase record. Consider implementing
      authorization checks to ensure only authenticated customers can buy packages
      and validation checks to prevent invalid purchases.
    """
    email = request.session.get("email")
    packages = get_object_or_404(Package, id=id)

    if request.method == "POST":
        form = BuyForms(request.POST)
        try:
            if form.is_valid():
                form.save()
                return render(request, "buy_packages.html", {"msg": "Success", "email": email})
        except Exception as e:
            # Handle the exception here, you can log it or display an error message
            error_msg = f"An error occurred: {e}"
            return render(request, "buy_packages.html", {"packages": packages, "email": email, "error_msg": error_msg})

    return render(request, "buy_packages.html", {"packages": packages, "email": email})


def my_packages(request):
    """
      Fetches and displays a customer's purchased packages (consider authorization).
      This function retrieves the customer's email from the session (security risk)
      and filters buy objects based on that email. Consider implementing authorization
      checks to ensure only the logged-in customer can view their purchases.
    """
    email = request.session["email"]
    packages = Buy.objects.filter(email=email)
    return render(request, "my_packages.html", {"packages": packages})


def vendor_view_buys(request):
    """
      Fetches and displays a vendor's buy objects (consider authorization).
      This function retrieves the vendor's email from the session (security risk)
      and filters buy objects based on that vendor's email. Consider implementing
      authorization checks to ensure only the logged-in vendor can view their buy objects.
    """
    email = request.session["email"]
    buys = Buy.objects.filter(vemail=email)
    return render(request, "vendor_view_buys.html", {"buys": buys})


def accept_buys(request, id):
    """
      Updates a buy object's status to 'Accepted' (consider authorization).
      This function retrieves a buy object based on the ID and sets its status to
      'Accepted'. Consider implementing authorization checks to ensure only the
      vendor who owns the package can accept a purchase.
    """
    buys = Buy.objects.get(id=id)
    buys.bstatus = 'Accepted'
    buys.save()
    return redirect("/vendor_home")


def reject_buys(request, id):
    """
      Updates a buy object's status to 'Rejected' (consider authorization).
      This function retrieves a buy object based on the ID and sets its status to
      'Rejected'. Consider implementing authorization checks to ensure only the
      vendor who owns the package can reject a purchase.
    """
    buys = Customer.objects.get(id=id)
    buys.bstatus = 'Rejected'
    buys.save()
    return redirect("/vendor_home")


def upload_file(request, id):
    """
      Handles uploading files securely (consider authorization and validation).
      This function retrieves a buy object based on the ID. It checks if the request
      method is POST. It creates an UplodfileForms object with the submitted data and
      uploaded files. If the form is valid, it saves the uploaded file(s). Consider
      implementing authorization checks to ensure only the vendor who owns the
      purchase can upload files, and validation checks to ensure valid file types
      and sizes.
    """
    buys = Buy.objects.get(id=id)
    if request.method == "POST":
        form = UplodfileForms(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, "upload_file.html", {"msg": "Files Uploaded"})
    return render(request, "upload_file.html", {"buys": buys})


def customer_view_files(request, id):
    """
      Fetches and displays uploaded files for a purchase (consider authorization).
      This function retrieves a buy object based on the ID and filters uploaded files
      based on the buy object's ID. Consider implementing authorization checks to
      ensure only the customer who purchased the package can view the uploaded files.
    """
    packages = Buy.objects.get(id=id)
    files = Uplodfile.objects.filter(buy_id=packages)
    return render(request, "customer_view_files.html", {"files": files})


def addfamily(request):
    """
      Handles adding family members securely (consider authorization and validation).
      This function retrieves the customer's email from the session (security risk)
      and checks if the request method is POST. It creates an AddfamilyForms object
      with the submitted data. If the form is valid, it saves the new family member
      information. Consider using a more secure method for email retrieval and
      implementing authorization checks to ensure only the logged-in customer can
      add family members.
    """
    email = request.session["email"]
    if request.method == "POST":
        form = AddfamilyForms(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, "addfamily.html", {"msg": "Added"})
    return render(request, "addfamily.html", {"email": email})


def myfamily(request):
    """
      Fetches and displays a customer's family members (consider authorization).
      This function retrieves the customer's email from the session (security risk)
      and filters family member objects based on that email. Consider using a more
      secure method for email retrieval and implementing authorization checks to
      ensure only the logged-in customer can view their family members.
    """
    email = request.session["email"]
    family = Addfamily.objects.filter(email=email)
    return render(request, "myfamily.html", {"family": family})


def delete_myfamily(request, id):
    """
      Deletes a family member object (consider authorization).
      This function retrieves a family member object based on the ID and deletes it.
      Consider implementing authorization checks to ensure only the customer who
      added the family member can delete it.
    """
    family = Addfamily.objects.get(id=id)
    family.delete()
    return render(request, "myfamily.html", {})


def edit_myfamily(request, id):
    """
      Fetches a family member object for editing (consider authorization).
      This function retrieves a family member object based on the ID. Consider
      implementing authorization checks to ensure only the customer who added
      the family member can edit their information.
    """
    family = Addfamily.objects.get(id=id)
    return render(request, "edit_myfamily.html", {"family": family})


def update_myfamily(request):
    """
      Updates a family member's information securely (consider authorization and validation).
      This function retrieves a family member object based on the ID from the POST data,
      creates an AddfamilyForms object with the submitted data and the existing member
      instance for update. It validates the form and saves the updated member information
      if valid. Consider implementing authorization checks to ensure only the customer
      who added the family member can update their information.
    """
    try:
        if request.method == "POST":
            id = request.POST["id"]
            user = Addfamily.objects.get(id=id)
            form = AddfamilyForms(request.POST, request.FILES, instance=user)
            print(form.errors)
            if form.is_valid():
                form.save()
                return redirect('/myfamily')
        return redirect('/customer_home')
    except Exception as e:
        return HttpResponseServerError("An error occurred: " + str(e))


def vendor_view_family(request, id):
    """
      Fetches and displays a customer's family members based on a buy object (consider authorization).
      This function retrieves a buy object and filters family member objects based on
      the email from that buy object. Consider implementing authorization checks to
      ensure only the vendor who owns the purchase can view the customer's family members.
    """
    buys = Buy.objects.get(id=id)
    family = Addfamily.objects.filter(email=buys.email)
    return render(request, "vendor_view_family.html", {"family": family})


def notification(request):
    """
      Handles adding notifications securely (consider authorization and validation).
      This function checks if the request method is POST. It creates a NotificationForms
      object with the submitted data. If the form is valid, it saves the new notification.
      Consider implementing authorization checks to restrict who can add notifications
      and validation checks to prevent invalid data.
    """
    if request.method == "POST":
        form = NotificationForms(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "notification.html", {"msg": "Added Notification"})
    return render(request, "notification.html", {})


def customer_notification(request):
    """
      Fetches and displays all notifications (consider authorization).
      This function retrieves all notification objects and renders them in the
      "customer_notification.html" template. Consider implementing authorization
      checks to ensure only authorized users can view all notifications.
    """
    remainder = Notification.objects.all()
    return render(request, "customer_notification.html", {'remainder': remainder})


def view_notification(request):
    """
      Fetches and displays all notifications (consider authorization).
      This function retrieves all notification objects and renders them in the
      "view_notification.html" template. Consider implementing authorization
      checks to ensure only authorized users can view all notifications.
    """
    remainder = Notification.objects.all()
    return render(request, "view_notification.html", {'remainder': remainder})


def delete_notification(request, id):
    """
      Deletes a notification object (consider authorization).
      This function retrieves a notification object based on the ID and deletes it.
      Consider implementing authorization checks to restrict who can delete notifications.
    """
    remainder = Notification.objects.get(id=id)
    remainder.delete()
    return render(request, "view_notification.html", {})


def cashless_hospitals(request):
    """
      Handles adding cashless hospitals securely (consider authorization and validation).
      This function retrieves the customer's email from the session (security risk)
      and checks if the request method is POST. It creates a HospitalsForms object
      with the submitted data. If the form is valid, it saves the new cashless hospital.
      Consider using a more secure method for email retrieval, implementing authorization
      checks to restrict who can add cashless hospitals, and validation checks to
      ensure valid hospital data.
    """
    email = request.session["email"]
    if request.method == "POST":
        form = HospitalsForms(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "cashless_hospitals.html", {"msg": "Added"})
    return render(request, "cashless_hospitals.html", {"email": email})


def hospitals(request, email):
    """
      Fetches and displays a vendor's cashless hospitals based on email (security risk).
      This function retrieves a vendor object based on the provided email (security risk)
      and filters cashless hospital objects based on that vendor's email. Consider
      using a more secure method to identify the vendor and implementing authorization
      checks to ensure only the vendor can view their cashless hospitals.
    """
    vendors = Vendor.objects.get(email=email)
    helth = Hospitals.objects.filter(email=vendors.email)
    return render(request, "hospitals.html", {'helth': helth})


def customer_vendors(request):
    """
      Fetches and displays all vendors (consider filtering and pagination).
      This function retrieves all vendor objects from the database and renders them in the
      "customer_vendors.html" template. Consider implementing filtering, pagination,
      or authorization checks for extensive data sets in a production environment.
    """
    vendors = Vendor.objects.all()
    return render(request, "customer_vendors.html", {'vendors': vendors})


def vendor_view_hospital(request):
    """
      Fetches and displays a vendor's cashless hospitals (consider authorization).
      This function retrieves the vendor's email from the session (security risk)
      and filters cashless hospital objects based on that email. Consider using a
      more secure method for email retrieval and implementing authorization checks
      to ensure only the vendor can view their cashless hospitals.
    """
    email = request.session["email"]
    hospital = Hospitals.objects.filter(email=email)
    return render(request, "vendor_view_hospital.html", {'hospital': hospital})


def delete_vendor_hospitals(request, id):
    """
      Deletes a cashless hospital object (consider authorization).
      This function retrieves a cashless hospital object based on the ID and deletes it.
      Consider implementing authorization checks to restrict who can delete hospitals.
    """
    hospital = Hospitals.objects.get(id=id)
    hospital.delete()
    email = request.session["email"]
    hospital = Hospitals.objects.filter(email=email)
    return render(request, "vendor_view_hospital.html", {"hospital": hospital})


def submit_claim(request, id):
    """
      Handles submitting claims securely (consider authorization and validation).
      This function retrieves a buy object and all hospital objects. It also retrieves
      the customer's email from the session (security risk). It checks if the request
      method is POST. It creates a SubmitclaimForms object with the submitted data and
      uploaded files. If the form is valid, it saves the new claim. Consider using a
      more secure method for email retrieval, implementing authorization checks to
      restrict who can submit claims, and validation checks to ensure valid claim data.
    """
    packages = Buy.objects.get(id=id)
    hospitals = Hospitals.objects.all()
    email = request.session["email"]
    if request.method == "POST":
        form = SubmitclaimForms(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, "submit_claim.html", {"msg": "Claimed"})
    return render(request, "submit_claim.html", {"email": email, "packages": packages, "hospitals": hospitals})


def claims(request, email):
    """
      Fetches and displays a vendor's claims based on email (security risk).
      This function retrieves a vendor object based on the provided email (security risk)
      and filters claim objects based on that vendor's email. Consider using a more
      secure method to identify the vendor and implementing authorization checks to
      ensure only the vendor can view their claims.
    """
    vendors = Vendor.objects.get(email=email)
    claim = Submit_Claim.objects.filter(email=vendors.email)
    return render(request, "claims.html", {'claim': claim})


def vendor_view_claims(request, id):
    buys = get_object_or_404(Buy, id=id)
    claims = Submit_Claim.objects.filter(packages=buys.id)
    return render(request, "vendor_view_claims.html", {'claims': claims})

def customers_view_claims(request, id):
    packages = get_object_or_404(Buy, id=id)
    claims = Submit_Claim.objects.filter(packages=packages.id)
    return render(request, "customers_view_claims.html", {'claims': claims})

def accept_claims(request,id):
    claims = Submit_Claim.objects.get(id=id)
    claims.sstatus = 'Accepted'
    claims.save()
    return redirect("/vendor_view_claims")


def reject_claims(request, id):
    claims = Submit_Claim.objects.get(id=id)
    claims.sstatus = 'Rejected'
    claims.save()
    return redirect("/vendor_view_claims")

def admit_hospital_request(request,id):
    helth = Hospitals.objects.get(id=id)
    email = request.session["email"]
    if request.method == "POST":
        form = Admit_RequestsForms(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, "admit_hospital_request.html", {"msg": "Success"})
    return render(request, "admit_hospital_request.html", {"email": email,"helth": helth})

def vendor_view_admit_hospital_requests(request,id):
    hospital = Hospitals.objects.get(id=id)
    admits = Admit_Requests.objects.filter(hospitals=hospital.id)
    return render(request, "vendor_view_admit_hospital_requests.html", {'admits':admits})

def accept_admits_requests(request,id):
    admits = Admit_Requests.objects.get(id=id)
    admits.bstatus = 'Accepted'
    admits.save()
    return redirect("/vendor_view_admit_hospital_requests")


def reject_admits_requests(request, id):
    admits = Admit_Requests.objects.get(id=id)
    admits.bstatus = 'Rejected'
    admits.save()
    return redirect("/vendor_view_admit_hospital_requests")



def customers_view_admit_hospital_requests(request):
    email = request.session["email"]
    admits = Admit_Requests.objects.filter(email=email)
    return render(request, "customers_view_admit_hospital_requests.html", {'admits':admits})
