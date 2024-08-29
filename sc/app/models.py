from django.db import models
from django.contrib.auth.models import User
import pickle
import os
import pandas as pd
import numpy as np

# Create your models here.
STATE_CHOICES = (
    ('Andaman and Nicobar Islands','Andaman and Nicobar Islands'),
    ('Andhra Pradesh','Andhra Pradesh'),
    ('Arunachal Pradesh','Arunachal Pradesh'),
    ('Assam','Assam'),
    ('Bihar','Bihar'),
    ('Chandigarh','Chandigarh'),
    ('Chhattisgarh','Chhattisgarh'),
    ('Daman and Diu','Daman and Diu'),
    ('Dadra and Nagar Haveli','Dadra and Nagar Haveli'),
    ('Delhi','Delhi'),
    ('Goa','Goa'),
    ('Gujarat','Gujarat'),
    ('Haryana','Haryana'),
    ('Himachal Pradesh','Himachal Pradesh'),
    ('Jammu and Kashmir','Jammu and Kashmir'),
    ('Jharkhand','Jharkhand'),
    ('Karnataka','Karnataka'),
    ('Kerala','Kerala'),
    ('Lakshadweep','Lakshadweep'),
    ('Madhya Pradesh','Madhya Pradesh'),
    ('Maharashtra','Maharashtra'),
    ('Manipur','Manipur'),
    ('Mizoram','Mizoram'),
    ('Meghalaya','Meghalaya'),
    ('Nagaland','Nagaland'),
    ('Odisha','Odisha'),
    ('Puducherry','Puducherry'),
    ('Punjab','Punjab'),
    ('Rajasthan','Rajasthan'),
    ('Sikkim','Sikkim'),
    ('Tamil Nadu','Tamil Nadu'),
    ('Telangana','Telangana'),
    ('Tripura','Tripura'),
    ('Uttar Pradesh','Uttar Pradesh'),
    ('Uttarakhand','Uttarakhand'),
    ('West Bengal','West Bengal'),
)

CATEGORY_CHOICES=(
    ('BR','beverage '),
    ('BF','breakfast'),
    ('DT','dessert'),
    ('MC','main course'),
    ('SP','soup'),
    ('CH','chapati'),
)

base_dir = 'C:\\Users\\SANIYA\\OneDrive\\Desktop\\SC sem 6\\sc' 


# Define the pickle directory
pickle_dir = os.path.join(base_dir, 'pickle')

# Load similarity1.pkl
similarity1_path = os.path.join(pickle_dir, 'similarity1.pkl')
with open(similarity1_path, 'rb') as file:
    similarity1 = pickle.load(file)

# Load similarity2.pkl
similarity2_path = os.path.join(pickle_dir, 'similarity2.pkl')
with open(similarity2_path, 'rb') as file:
    similarity2 = pickle.load(file)

class Product(models.Model):
    id = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=255)
    ProductId = models.CharField(max_length=20)
    food_name = models.CharField(max_length=100)
    #food_category = models.CharField(choices=CATEGORY_CHOICES, max_length=100)
    food_category = models.CharField(max_length=100)
    sub_category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    Image = models.CharField(max_length=255)

    def __str__(self):
        return self.food_name

    def get_recommendations(self):
        # Assuming similarity1 is already calculated and available

        # Get the index of the current product
        product_index = self.id - 1

        # Get similarity scores for all products compared to the current product
        similarity_scores = similarity1[product_index]

        # Sort similarity scores in descending order and select top similar products
        similar_product_indices = similarity_scores.argsort()[:-6:-1]  # Exclude the current product itself
        similar_products = [Product.objects.get(pk=index + 1) for index in similar_product_indices]

        # Convert similar products to dictionary format for rendering
        recommendations = []
        for product in similar_products:
            recommendations.append({
                "pk": product.pk,
                "food_name": product.food_name,
                "image_title": product.Image,
                "food_category": product.food_category,
                "price": product.price
            })

        return recommendations
    
# class Product(models.Model):
#     title = models.CharField(max_length=100)
#     selling_price = models.FloatField()
#     discounted_price = models.FloatField()
#     description = models.TextField()
#     #context = models.TextField(default=' ')
#     customization = models.TextField(default=' Not Available')
#     category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
#     #category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
#     product_image = models.ImageField(upload_to='product')
#     def __str__(self):
#         return self.title 
    
class Customer(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    village = models.CharField(max_length=200)
    landmark = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    mobile = models.IntegerField(default=0,help_text = "Please enter 10 digits valid Number")
    pincode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES,max_length=100)
    def __str__(self):
        return self.name
    
class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
       
    @property
    def total_cost(self):
        return self.quantity * self.product.price


STATUS_CHOICES = (
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On The Way','On The Way'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel'),
    ('Pending','Pending'),
)

class Payment(models.Model):
    user =  models.ForeignKey(User,on_delete=models.CASCADE)
    amount = models.FloatField()
    razorpay_order_id = models.CharField(max_length=100,blank=True,null=True)
    razorpay_payment_status = models.CharField(max_length=100,blank=True,null=True)
    razorpay_payment_id = models.CharField(max_length=100,blank=True,null=True)
    paid = models.BooleanField(default=False)

class OrderPlaced(models.Model):
    user =  models.ForeignKey(User,on_delete=models.CASCADE)
    customer =  models.ForeignKey(Customer,on_delete=models.CASCADE)
    product =  models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status =  models.CharField(max_length=50,choices=STATUS_CHOICES, default='Pending')
    payment = models.ForeignKey(Payment,on_delete=models.CASCADE,default="")
    @property
    def total_cost(self):
        return self.quantity * self.product.price
    
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

class Feedback(models.Model):
    name=models.CharField(max_length=200)
    email=models.EmailField()
    comment=models.TextField()
    def __str__(self):
        return self.name