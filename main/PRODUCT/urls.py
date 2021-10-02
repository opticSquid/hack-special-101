from django.contrib import admin
from django.urls import path, include 
from . import views

app_name="PRODUCT"

urlpatterns = [
   path('search/',views.search_p,name='search'),
   path('add_to_cart/',views.add_to_cart,name='add_to_cart'),
  
    # path('products/<slug:pk>',views.all_products,name='detailprod_page'),
   ###############            Cart urls            ##########################
 
    path('add_to_cart/',views.add_to_cart,name='add_to_cart'),
    path('view_cart/',views.view_cart,name='view_cart'),
    path('plus_cart/',views.plus_cart,name='plus_cart'),
   #path('buy_now_checkout/',views.buy_now_checkout,name='buy_now_checkout'),
    path('minus_cart/',views.minus_cart,name='minus_cart'),
    path('delete_cart/',views.remove_cart,name='delete_cart'),
    path('checkout/',views.checkout,name='checkout'),
    path('add_tipcoin/',views.add_tipcoin,name='add_tipcoin'),
    path('reduce_tipcoin/',views.reduce_tipcoin,name='reduce_tipcoin'),
    path('add_address/',views.add_address,name='add_address'),
  #################                PAYMENT             #################################
    path('payment_done/',views.payment_done,name="payment_done"),
    #path('success/',views.payment_success,name="payment-success"),

]