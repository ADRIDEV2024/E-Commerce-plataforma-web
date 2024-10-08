from django.db.models.signals import post_save 
from django.conf import settings 
from django.db import models
from django.db.models import Sum
from django.shortcuts import reverse
from django_countries.fields import CountryField


class CategoryChoices(models.TextChoices):
    SHIRTS = "S", "Shirts"
    PANTS = "P", "Pants"
    JACKETS = "J", "Jackets"
    COATS = "C", "Coats"
    HOODIES = "H", "Hoodies"
    SPORTS = "SP", "Sports"

class SizeChoices(models.TextChoices):
    EXTRA_SMALL = "XS", "Extra Small"
    SMALL = "S", "Small"
    LARGE = "L", "Large"
    MEDIUM = "M", "Medium"
    EXTRA_LARGE = "XL", "Extra Large"

class AddressChoices(models.TextChoices):
    BILLING = "B", "Billing"
    SHIPPING = "S", "Shipping"

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    customer_id = models.CharField(max_length=50, blank=True, null=True)
    one_click_purchasing = models.BooleanField(default=False)
    
    def __str__(self):
        self.user.username
    
class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    label = models.CharField(choices=SIZE_CHOICES, max_length=2)
    
    description = models.TextField()
    image = models.ImageField(upload_to = "items/)
    
    def __str__(self):
        self.title
    
def get_absolute_url(self):
        return reverse("That´s my shirt!:product", kwargs={"slug": self.slug})
        
def get_add_to_cart_url(self):
        return reverse("That´s my shirt!:add-to-cart", kwargs={'slug': self.slug})

def get_remove_from_cart_url(self):
        return reverse("That´s my shirt!:remove-from-cart", kwargs={'slug': self.slug})

class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    
    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price
    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey('Address', related_name='shipping_address', on_delete=models.SET_NULL, 
                                         blank=True, null=True)
    billing_address = models.ForeignKey('Address', related_name='billing_address', on_delete=models.SET_NULL, 
                                         blank=True, null=True)
    payment = models.ForeignKey('Payment', on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey('Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)
    
def __str__(self):
        return f"Order {self.ref_code} by {self.user.username}
    
def get_total(self):
    total = 0
    for order_item in self.items.all():
            total += order_item.get_final_price()
    if self.coupon:
        total -= self.coupon.amount
    return total
