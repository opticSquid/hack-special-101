from django.db import models
from django.contrib.auth.models import User
# Create your models here.
import uuid
from django.db.models.base import Model
from django.utils import timezone



choice=(
    ('Fast Food','Fast Food'),
    ('Meal','Meal'),
    ('Dinner','Dinner'),
    ('Cookies','Cookies'),)


class Catagory(models.Model):
    cat_name=models.CharField(default='meal',choices=choice,max_length=30)
    def __str__(self):
        return self.cat_name
class Products(models.Model):
    Sub_catagory_p = models.ForeignKey(Catagory,on_delete=models.CASCADE,blank=False)
    custom_id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    name=models.CharField(max_length=100)
    image1=models.ImageField(upload_to='plantimage/')
    image2 = models.ImageField(upload_to='plantimage/',blank=True,null=True)
    #image3 = models.ImageField(upload_to='media/plantimage/',blank=True,null=True)
    description=models.TextField(max_length=1000)
  
    max_price=models.PositiveIntegerField(default=1)
    off_price=models.PositiveIntegerField(default=1)
    quantity=models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.name)
class Cart(models.Model):
    auth_user= models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    product_p=models.ForeignKey(Products,on_delete=models.CASCADE,blank=True)
    
    prod_quantity =models.PositiveIntegerField(default=1)
    toal_payable_amount=models.PositiveIntegerField(default=0,blank=True,null=True)
    cart_total=models.IntegerField(default=1)
    def __str__(self):
        return str(self.auth_user)+"'s   Cart"+str(self.prod_quantity)


################            adddress for user         ###############################
class Address(models.Model):
       user=models.ForeignKey(User,on_delete=models.CASCADE)
      
       f_add=models.CharField(max_length=1000,default='Full address')
      
       pin=models.CharField(max_length=8,default=71)
       ph_no=models.CharField(max_length=11,default=+91)
      
       def __str__(self):
           return str(self.f_add)+"  "+str(self.user)

######################    CHECKOUT AND PAYMENT ###############################

class Order(models.Model):
    Choices=(
        ("PLACED","PLACED"),
        ("SHIPPED","SHIPPED"),
        ("DELIVERED","DELIVERED"),
        ("CANCEL","CANCEL"),
    )
    customer_name=models.ForeignKey(User,on_delete=models.CASCADE)
    o_palced_name=models.ForeignKey(Products,on_delete=models.CASCADE,null=True,blank=True)
    #o_palced_order_id=models.CharField(max_length=50,blank=True,null=True)
    date_time=models.DateField(default=timezone.now,auto_created=True)
    order_price=models.FloatField(default=1,null=True,blank=True)
    user_address=models.ForeignKey(Address,on_delete=models.CASCADE)
    order_quantity=models.IntegerField(default=1,blank=True,null=True)
    is_placed=models.BooleanField(default=False)
    placed=models.CharField(max_length=20,default='PLACED',choices=Choices)

    def __str__(self):
        return str(self.customer_name)+"'s order ---Paid="+str(self.is_placed)+"-----Current Status="+str(self.placed)

class Tip(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    
    tips_count=models.PositiveIntegerField(default=1,blank=True,null=True)
    def __str__(self) -> str:
        return str(self.user)+str("'s TIP")

class Order(models.Model):
    customer_name=models.ForeignKey(User,on_delete=models.CASCADE)
    o_palced_name=models.ForeignKey(Products,on_delete=models.CASCADE,null=True,blank=True)
    #o_palced_order_id=models.CharField(max_length=50,blank=True,null=True)
    #date_time=models.DateField(default=timezone.now,auto_created=True)
    order_price=models.FloatField(default=1,null=True,blank=True)
    user_address=models.ForeignKey(Address,on_delete=models.CASCADE)
    order_quantity=models.IntegerField(default=1,blank=True,null=True)
    is_placed=models.BooleanField(default=False)
    tip_coin=models.IntegerField(default=1,null=True,blank=True)
    def __str__(self):
        return str(self.customer_name)