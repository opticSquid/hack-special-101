from django.contrib import admin
from .models import Catagory ,Products,Address,Cart,Tip,Order

# Register your models here.
admin.site.register(Catagory)
admin.site.register(Products)
admin.site.register(Cart)
admin.site.register(Address)
admin.site.register(Tip)
admin.site.register(Order)