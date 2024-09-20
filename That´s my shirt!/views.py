from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from django.views.generic import ListView, DetailView, View

from .forms import CheckoutForm, CouponForm, RefundForm, PaymentForm
from .models import Item, OrderItem, Order, Address, Payment, Coupon, Refund, UserProfile


def products(request):
    """
    Handles the request to display all products on the products page.

    This function is responsible for retrieving all items from the database
    and rendering them on the 'products.html' template. It creates a context
    dictionary containing all the items and passes it to the template for rendering.

    :Params:
        request (HttpRequest): The HTTP request object.

    :Return:
        HttpResponse: The rendered 'products.html' template with the context data.
    """
    context = {
        'items': Item.objects.all()
    }
    return render(request, "products.html", context)


def is_valid_form(values):
    return all(field != '' for field in values)


class CheckoutView(View):
     """
    Handles the checkout process for the e-commerce platform.

    The CheckoutView class is responsible for managing the checkout process.
    It retrieves the user's current order, initializes the necessary forms,
    and renders the checkout page with the appropriate context. If no active
    order is found, it redirects the user to the checkout page with an informational message.

    Methods:
        get(self, *args, **kwargs): Handles GET requests to display the checkout page.
    """
     def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            form = CheckoutForm()
            context = {
                'form': form,
                'couponform': CouponForm(),
                'order': order,
                'DISPLAY_COUPON_FORM': True
            }

            self.add_default_addresses(context)

            return render(self.request, "checkout.html", context)
