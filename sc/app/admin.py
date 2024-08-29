from django.contrib import admin
from . models import Feedback, Product, Customer, Cart, Payment,OrderPlaced, Wishlist
from django.utils.html import format_html
from django.urls import reverse
from django.contrib.auth.models import Group

# Register your models here.
@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'description', 'ProductId', 'price', 'food_name', 'food_category', 'sub_category', 'Image')

# admin.site.register(Product, ProductModelAdmin)

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','village','city','state','pincode']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    def products(self, obj):
        link = reverse("admin:app_product_change", args=[obj.product.id])
        return format_html('<a href="{}">{}</a>', link, obj.product.food_name)

@admin.register(Payment)
class PaymentModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','amount','razorpay_order_id','razorpay_payment_status','razorpay_payment_id','paid']

@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','customers','products','quantity','ordered_date','status','payments']

    def customers(self,obj):
        link=reverse('admin:app_customer_change',args=[obj.customer.pk])
        return format_html('<a href="{}">{}</a>',link,obj.customer.name)
    
    def products(self,obj):
        link = reverse("admin:app_product_change", args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>',link,obj.product.food_name)  # Change 'title' to 'food_name'
    
    def payments(self,obj):
        link = reverse("admin:app_payment_change", args=[obj.payment.pk])
        return format_html('<a href="{}">{}</a>',link,obj.payment.razorpay_payment_id)

@admin.register(Wishlist)
class WishlistModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','product']

@admin.register(Feedback)
class FeedbackModelAdmin(admin.ModelAdmin):
    list_display=['name', 'email', 'comment']


admin.site.unregister(Group)