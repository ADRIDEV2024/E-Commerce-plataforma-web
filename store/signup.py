from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from models import Customer

class SignupView(View):
    template_name = 'signup.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        customer = self.create_customer_from_post_data(request.POST)
        error_message = self.validate_customer(customer)

        if not error_message:
            self.register_customer(customer)
            return redirect('home')
        else:
            return self.render_with_error(request, error_message, customer)

    def create_customer_from_post_data(self, post_data):
        return Customer(
            first_name=post_data.get('firstname'),
            last_name=post_data.get('lastname'),
            phone=post_data.get('phone'),
            email=post_data.get('email'),
            password=post_data.get('password')
        )

    def validate_customer(self, customer):
        validations = [
            (lambda: not customer.first_name, "Please Enter your First Name !!"),
            (lambda: len(customer.first_name) < 5, 'First Name must be 5 char long or more'),
            (lambda: not customer.last_name, 'Please Enter your Last Name'),
            (lambda: len(customer.last_name) < 5, 'Last Name must be 5 char long or more'),
            (lambda: not customer.phone, 'Enter your Phone Number'),
            (lambda: len(customer.phone) < 10, 'Phone Number must be 10 char Long'),
            (lambda: len(customer.password) < 8, 'Password must be 8 char long'),
            (lambda: len(customer.email) < 5, 'Email must be 5 char long'),
            (customer.isExists, 'Email Address Already Registered..')
        ]

        for condition, error_message in validations:
            if condition():
                return error_message
        return None

    def register_customer(self, customer):
        customer.password = make_password(customer.password)
        customer.register()

    def render_with_error(self, request, error_message, customer):
        context = {
            'error': error_message,
            'values': {
                'first_name': customer.first_name,
                'last_name': customer.last_name,
                'phone': customer.phone,
                'email': customer.email
            }
        }
        return render(request, self.template_name, context)

