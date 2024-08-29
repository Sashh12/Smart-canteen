from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, Q, F
from django.views import View
from . models import Feedback, OrderPlaced, Payment, Product, Customer, Cart, Wishlist
from . forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.http import HttpResponseNotFound, JsonResponse
import razorpay
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from decimal import Decimal
import pickle
import os
import pandas as pd
import numpy as np
from datetime import datetime


# Create your views here.

def recommend_by_time():
    now = datetime.now()
    current_time = now.time()

    if datetime.strptime('06:00:00', '%H:%M:%S').time() <= current_time <= datetime.strptime('10:59:59', '%H:%M:%S').time():
        return recommend_breakfast()
    elif datetime.strptime('11:00:00', '%H:%M:%S').time() <= current_time <= datetime.strptime('15:59:59', '%H:%M:%S').time():
        return recommend_main_course()
    elif datetime.strptime('16:00:00', '%H:%M:%S').time() <= current_time <= datetime.strptime('20:59:59', '%H:%M:%S').time():
        return recommend_soup()
    elif datetime.strptime('21:00:00', '%H:%M:%S').time() <= current_time <= datetime.strptime('23:59:59', '%H:%M:%S').time():
        return recommend_main_course()
    else:
        return [{"food_name": "No recommendations for the current time.", "food_category": "","Image":""}]

# Define functions to recommend items for different meal times
def recommend_breakfast():
    # Filter breakfast items
    breakfast_items = Product.objects.filter(food_category='breakfast')
    if breakfast_items.exists():
        # Return recommended breakfast items
        return breakfast_items.values('food_name', 'food_category', 'Image','pk')
    else:
        return [{"food_name": "No breakfast items available.", "food_category": "", "Image": "","pk":""}]

def recommend_main_course():
    # Filter main course items
    main_course_items = Product.objects.filter(food_category='main course')
    if main_course_items.exists():
        # Return recommended main course items
        return main_course_items.values('food_name', 'food_category', 'Image','pk')
    else:
        return [{"food_name": "No main course items available.", "food_category": "", "Image": "","pk":""}]

def recommend_soup():
    # Filter soup items
    soup_items = Product.objects.filter(sub_category='snack')
    if soup_items.exists():
        # Return recommended soup items
        return soup_items.values('food_name', 'food_category', 'Image','pk')
    else:
        return [{"food_name": "No soup items available.", "food_category": "", "Image": "","pk":""}]

@login_required
def home(request):
    # Call the recommend_by_time function to generate recommendations
    recommendations1 = recommend_by_time()

    for recommendation in recommendations1:
        if 'pk' not in recommendation or not recommendation['pk']:
            # If the 'pk' is empty, set it to a default value or handle it as needed
            recommendation['pk'] = 0  # Set a default value

    # Render the template and pass the recommendations
    return render(request, 'app/home.html', {'recommendations1': recommendations1})

# @login_required 
# def home(request):
#     # totalitem = 0
#     # if request.user.is_authenticated:
#     #     totalitem=len(Cart.objects.filter(user=request.user))
#     return render(request,"app/home.html",locals())

@login_required 
def about(request):
    return render(request,'app/about.html')

@login_required 
def contact(request):
    return render(request,'app/contact.html')

@login_required 
def feedback(request):
    return render(request,'app/Feedback.html')

@login_required 
def ByCategory(request):
    return render(request,'app/ByCategory.html')

@login_required 
def ByMeaning(request):
    return render(request,'app/ByMeaning.html')

@login_required 
def ByColour(request):
    return render(request,'app/ByColour.html')

@login_required 
def ByCrystals(request):
    return render(request,'app/ByCrystals.html')

@login_required 
def Choose(request):
    return render(request,'app/Choose.html')

@login_required 
def Cleanse(request):
    return render(request,'app/Cleanse.html')

@login_required 
def Customize(request):
    return render(request,'app/Customize.html')

@method_decorator(login_required,name='dispatch')
class CategoryView(View):
    def get(self,request,val): 
       product = Product.objects.filter(food_category=val)
       food_name = val
       return render(request, {'product': product, 'food_name':food_name})
    
@method_decorator(login_required,name='dispatch')
# class ProductDetail(View):
#     def get(self,request,pk):
#         product = Product.objects.get(pk=pk)
#         wishlist = Wishlist.objects.filter(Q(product=product) & Q(user=request.user))
#         return render(request, 'app/productdetail.html',locals())


   
class CustomerRegistrationView(View):
    def get(self,request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html',locals())
    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Congratulations! User Register Successfully")
        else:
            messages.warning(request,"Inavalid Input Data")
        return render(request, 'app/customerregistration.html',locals())

@method_decorator(login_required,name='dispatch')    
class ProfileView(View):
    def get(self,request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html',locals())
    def post(self,request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            village = form.cleaned_data['village']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            pincode = form.cleaned_data['pincode']

            reg = Customer(user=user,name=name,village=village,city=city,mobile=mobile,state=state,pincode=pincode)
            reg.save()
            messages.success(request, "Congratulations! Profile Saved Successfully")
        else:
            messages.warning(request,"Invalid Input Data")
        return render(request, 'app/profile.html',locals())

@login_required    
def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html',locals())

@method_decorator(login_required,name='dispatch')
class updateAddress(View):
    def get(self,request,pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        return render(request, 'app/updateAddress.html',locals())
    def post(self,request,pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.village = form.cleaned_data['village']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.state = form.cleaned_data['state']
            add.pincode = form.cleaned_data['pincode']
            add.save()
            messages.success(request,"Congratulations! Profile Updated Successfully")
        else:
            messages.warning(request,"Invalid Input Data")
        return redirect("address")
    
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get("prod_id")
    product = Product.objects.get(id=product_id)
    
    # Check if the product is already in the cart for the current user
    existing_cart_item = Cart.objects.filter(user=user, product=product).first()
    if existing_cart_item:
        # If the product already exists in the cart, increase the quantity by 1
        existing_cart_item.quantity = F('quantity') + 1
        existing_cart_item.save()
        # messages.success(request, "Quantity updated successfully.")
    else:
        # If the product is not in the cart, add it to the cart with quantity 1
        Cart.objects.create(user=user, product=product)
        # messages.success(request, "Product added to cart successfully.")
    
    return redirect("/cart")

def show_cart(request):
    user = request.user
    cart_items = Cart.objects.filter(user=user)
    
    total_amount = 0
    for cart_item in cart_items:
        value = cart_item.quantity * cart_item.product.price
        total_amount += value
    
    
    return render(request, 'app/addtocart.html', {'cart_items': cart_items, 'total_amount': total_amount})

def show_wishlist(request):
    user = request.user
    product = Wishlist.objects.filter(user=user)
    return render(request, 'app/wishlist.html',locals())

@method_decorator(login_required,name='dispatch')
class checkout(View):
    def get(self,request):
        user=request.user
        add=Customer.objects.filter(user=user)
        cart_items=Cart.objects.filter(user=user)
        famount = 0
        for p in cart_items:
            value=p.quantity * p.product.price
            famount = famount + value
        totalamount = famount 
        razoramount = int(totalamount * 100)
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        data = {"amount" :razoramount, "currency":"INR","receipt":"order_rcptid_12"}
        payment_response = client.order.create(data=data)
        print(payment_response)
#         {'id': 'order_MfrhWc9zmEgv6L', 'entity': 'order', 'amount': 32900, 'amount_paid': 0, 'amount_due': 32900, 'currency': 'INR', 'receipt': 'order_rcptid_12', 'offer_id': None, 'status': 'created', 'attempts': 0, 'notes': [], 'created_at': 1695491366}
        order_id = payment_response['id']
        order_status = payment_response['status']
        if order_status == 'created':
            payment = Payment(
                user=user,
                amount=totalamount,
                razorpay_order_id = order_id,
                razorpay_payment_status = order_status
            )
            payment.save()
        return render(request, 'app/checkout.html',locals())

@login_required
def payment_done(request):
    order_id = request.GET.get('order_id')
    payment_id =  request.GET.get('payment_id')
    cust_id = request.GET.get('cust_id')
    #print("payment_done :oid=",order_id,"pid=",payment_id,"cid=",cust_id)
    user=request.user
    #return redirect("orders")
    customer = Customer.objects.get(id=cust_id)
    #To update payment status and payment payment id
    payment = Payment.objects.get(razorpay_order_id=order_id)
    payment.paid=True
    payment.razorpay_payment_id = payment_id
    payment.save()
    #To save order details
    cart=Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity,payment=payment).save()
        c.delete()
    return redirect("orders")

@login_required
def orders(request):
    order_placed=OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html',locals())


@login_required
def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        product = get_object_or_404(Product, id=prod_id)
        cart_item, created = Cart.objects.get_or_create(product=product, user=request.user)
        cart_item.quantity += 1
        cart_item.save()
        cart = Cart.objects.filter(user=request.user)
        amount = sum(p.quantity * p.product.price for p in cart)
        totalamount = amount

        data = {
            'quantity': cart_item.quantity,
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)

@login_required 
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        product = get_object_or_404(Product, id=int(prod_id))
        cart_item = get_object_or_404(Cart, product=product, user=request.user)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        cart = Cart.objects.filter(user=request.user)
        amount = sum(p.quantity * p.product.price for p in cart)
        totalamount = amount

        data = {
            'quantity': cart_item.quantity,
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)

@login_required
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        
        # Use get_object_or_404 to retrieve the cart item
        cart_item = get_object_or_404(Cart, product_id=prod_id, user=request.user)
        # Delete the cart item
        cart_item.delete()

        # Recalculate the amount and total amount after removing the item
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = sum(p.quantity * p.product.price for p in cart)
        totalamount = amount 

        # Prepare data to send back in the JSON response
        data = {
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)
 
def plus_wishlist(request):
    if request.method =='GET':
        prod_id = request.GET['prod_id']
        product = Product.objects.get(id=prod_id)
        user = request.user
        Wishlist(user=user, product=product).save()
        data={
            'message':'Item Sucessfully Added to Wishlist',
        }
        return JsonResponse(data)

 
def minus_wishlist(request):
    if request.method =='GET':
        prod_id = request.GET['prod_id']
        product = Product.objects.get(id=prod_id)
        user = request.user
        Wishlist.objects.filter(user=user, product=product).delete()
        data={
            'message':'Item Successfully Removed from Wishlist',
        }
        return JsonResponse(data)
    
@login_required    
def search(request):
    query = request.GET.get('search')
    # Check if the query is a valid decimal for price
    try:
        price = Decimal(query)
        products = Product.objects.filter(
            Q(food_name__icontains=query) |
            Q(food_category__icontains=query) |
            Q(sub_category__icontains=query) |
            Q(price__lte=query)  # Exact match for price
        )
    except:
        # If the query is not a valid decimal, filter without price
        products = Product.objects.filter(
            Q(food_name__icontains=query) |
            Q(food_category__icontains=query) |
            Q(sub_category__icontains=query)
        )

    return render(request, "app/search.html", {'products': products, 'query': query})



@login_required 
def feedback(request):
    if request.method=="POST":
        feedback=Feedback()
        name=request.POST.get('name')
        email=request.POST.get('email')
        comment=request.POST.get('comment')
        feedback.name=name
        feedback.email=email
        feedback.comment=comment
        feedback.save()
        # return HttpResponse("<center><h1>THANKS FOR YOUR FEEDBACK</h1><center>")
        return redirect("/")
    return render(request, 'app/feedback.html',locals())

# Write all the new views here

base_dir = 'C:\\Users\\SANIYA\\OneDrive\\Desktop\\SC sem 6\\sc' 

# Define the pickle directory
pickle_dir = os.path.join(base_dir, 'pickle')

# Load basic_dict.pkl
basic_dict_path = os.path.join(pickle_dir, 'basic_dict.pkl')
with open(basic_dict_path, 'rb') as file:
    basic_dict_data = pickle.load(file)

# Convert basic_dict_data to a DataFrame
food = pd.DataFrame(basic_dict_data)

# Load similarity1.pkl
similarity1_path = os.path.join(pickle_dir, 'similarity1.pkl')
with open(similarity1_path, 'rb') as file:
    similarity1 = pickle.load(file)

# Load similarity2.pkl
similarity2_path = os.path.join(pickle_dir, 'similarity2.pkl')
with open(similarity2_path, 'rb') as file:
    similarity2 = pickle.load(file)

def menu(request):
    # Retrieve all products from the database
    products = Product.objects.all()
    
    # Create a list to store zipped data
    zipped_data = []
    
    # Iterate over each product and zip its attributes
    for product in products:
        zipped_data.append((product.food_name, product.food_category, product.Image, product.price, product.id))
    
    # Pass the zipped data to the template
    context = {
        'zipped_data': zipped_data,
    }
    
    # Render the template with the data
    return render(request, 'app/menu.html', context)

def recommended_ui(request):
    return render(request, 'app/recommend.html')

def recommend_foods(request):
    if request.method == 'POST':
        # Get the user input from the form
        user_input = request.POST.get('user_input')

        # Recommendation code
        try:
            food_obj = Product.objects.get(food_name=user_input)
            food_index = food_obj.id  # Assuming the IDs are sequential starting from 1
            distances = similarity1[food_index]
            foods_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

            recommendations = []
            for i in foods_list:
                recommended_food = Product.objects.get(pk=i[0] + 1)  # Assuming primary keys are sequential starting from 1
                recommendations.append({
                    "pk": recommended_food.pk,  # Add the primary key here
                    "food_name": recommended_food.food_name,
                    "image_title": recommended_food.Image,
                    "food_category": recommended_food.food_category,
                    "price": recommended_food.price
                })

            same_category_recommendations = get_same_category_foods(user_input)

            return render(request, 'app/recommend.html', {
                'recommendations': recommendations,
                'same_category_recommendations': same_category_recommendations,
                'user_input': user_input
            })
        except Product.DoesNotExist:
            return HttpResponseNotFound("The requested item is currently not available.")

def get_same_category_foods(user_input):
    try:
        food_obj = Product.objects.get(food_name=user_input)
        sub_category = food_obj.sub_category
        same_category_foods = Product.objects.filter(sub_category=sub_category).exclude(food_name=user_input)[:9]

        same_category_recommendations = []
        for recommended_food in same_category_foods:
            same_category_recommendations.append({
                "pk": recommended_food.pk,  # Add the primary key here
                "food_name": recommended_food.food_name,
                "image_title": recommended_food.Image,
                "sub_category": recommended_food.sub_category,
                "price": recommended_food.price
            })

        return same_category_recommendations
    except Product.DoesNotExist:
        return []

def recommend(food):
    try:
        product = Product.objects.get(food_name=food)
        food_index = product.id - 1
        distances = similarity1[food_index]
        foods_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:7]

        recommendations = []
        for i in foods_list:
            similar_product = Product.objects.get(pk=i[0] + 1)
            recommendations.append({
                "pk": similar_product.pk,
                "food_name": similar_product.food_name,
                "image_title": similar_product.Image,
                "food_category": similar_product.food_category,
                "price": similar_product.price,
            })

        return recommendations
    except Product.DoesNotExist:
        return []

def same_recommend1(food):
    try:
        product = Product.objects.get(food_name=food)
        # food_index = product.id - 1
        sub_category = product.sub_category
        same_category_foods = Product.objects.filter(sub_category=sub_category).exclude(food_name=food)[:6]

        recommendations = []
        for recommended_food in same_category_foods:
            recommendations.append({
                "pk": recommended_food.pk,
                "food_name": recommended_food.food_name,
                "image_title": recommended_food.Image,
                "sub_category": recommended_food.sub_category,
                "price": recommended_food.price,
            })

        return recommendations
    except Product.DoesNotExist:
        return []

class ProductDetail(View):
    def get(self, request, pk):
        try:
            # Fetch the product from the database using the provided primary key (pk)
            product = Product.objects.get(id=pk)
            
            # Fetch the wishlist items for the current user and the specific product
            wishlist = Wishlist.objects.filter(Q(product=product) & Q(user=request.user))
            
            # Get recommendations for the current product
            recommendations = recommend(product.food_name)
            
            # Get same category recommendations for the current product
            same_category_recommendations = same_recommend1(product.food_name)

            context = {
                'product': product,
                'wishlist': wishlist,
                'recommendations': recommendations,
                'same_category_recommendations': same_category_recommendations,
            }
            return render(request, 'app/productdetail.html', context)
        except Product.DoesNotExist:
            # Handle the case where the product with the given primary key doesn't exist
            return HttpResponseNotFound("The requested product does not exist.")
        
