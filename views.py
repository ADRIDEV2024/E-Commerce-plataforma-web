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

    :Params: request (HttpRequest): The HTTP request object.

    :Return: HttpResponse: The rendered 'products.html' template with the context data.
    
    """
    context = {
        'items': Item.objects.all()
    }
    return render(request, "products.html", context)


def is_valid_form(values):
    return all(field != '' for field in values)


class CheckoutView(View):
     """  The CheckoutView class is responsible for managing the checkout process.
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
               
            self.add_default_addresses_(context)

            return render(self.request, "checkout.html", context)
            
        except ObjectDoesNotExist:
            messages.warning(self.request, "Oops :( maybe you don't have an active order")
            return redirect("That´s my shirt!:checkout")

     def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            #It attempts to retrieve the current order for the logged-in user that has not been completed.
            order = Order.objects.get(user=self.request.user, ordered=False)
            
            if form.is_valid():
                #If the form is valid, it processes the shipping and billing addresses using helper methods.
                self.handle_shipping_address(form, order)
                self.handle_billing_address(form, order)
                return redirect('That´s my shirt!:checkout')
            else:
                messages.warning(self.request, "Please correct the errors in the form")
                return redirect('That´s my shirt!:checkout')
                
        except ObjectDoesNotExist:
            messages.warning(self.request, "Oops :( maybe you don't have an active order")
            return redirect("That´s my shirt!:checkout")

     def add_default_addresses_(self, context):
        shipping_address = Address.objects.filter(
            user=self.request.user,
            address_type='S',
            default=True
        ).first()
        if shipping_address:
            context['default_shipping_address'] = shipping_address

        billing_address = Address.objects.filter(
            user=self.request.user,
            address_type='B',
            default=True
        ).first()
        if billing_address:
            context['default_billing_address'] = billing_address

        def handle_shipping_address(self, form, order):
          use_default_shipping = form.cleaned_data.get("use_default_shipping")
          if use_default_shipping:
            address = Address.objects.filter(
                user=self.request.user,
                address_type="S",
                default=True
            ).first()
            if address:
                order.shipping_address = address
                order.save()
            else:
                messages.info(self.request, "No default shipping address available")
          else:
            self.save_new_address(form, order, 'S', 'shipping')

        def handle_billing_address(self, form, order):
          same_billing_address = form.cleaned_data.get('same_billing_address')
          if same_billing_address:
            billing_address = order.shipping_address
            billing_address.pk = None
            billing_address.save()
            billing_address.address_type = 'B'
            billing_address.save()
            order.billing_address = billing_address
            order.save()
          else:
            self.save_new_address(form, order, 'B', 'billing')

        def save_new_address(self, form, order, address_type, prefix):
            address1 = form.cleaned_data.get(f"{prefix}_address")
            address2 = form.cleaned_data.get(f"{prefix}_address2")
            country = form.cleaned_data.get(f"{prefix}_country")
            zip_code = form.cleaned_data.get(f"{prefix}_zip")

            if is_valid_form([address1, country, zip_code]):
                address = Address(
                    user=self.request.user,
                    street_address=address1,
                    apartment_address=address2,
                    country=country,
                    zip=zip_code,
                    address_type=address_type
                )
                address.save()
                if address_type == 'S':
                    order.shipping_address = address
                else:
                    order.billing_address = address
                order.save()

                if address_type == 'S':
                    set_default = form.cleaned_data.get('set_default_shipping')
                    if set_default:
                        address.default = True
                        address.save()
            else:
                messages.info(self.request, f"Please fill in the required {prefix} address fields")
