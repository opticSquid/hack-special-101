from django.http.response import HttpResponse
from django.shortcuts import render ,redirect
from .models import Products,Address,Cart,Tip,Order
from django.contrib.auth.decorators import login_required
from django.db.models.query_utils import Q
from django.core.mail import mail_admins ,send_mail
from django.http import JsonResponse
import razorpay
# Create your views here.
def search_p(request):
 if request.method=='POST':
    query = request.POST['search_query']
    if query:
       print(query)
       if len(query) >= 100:
           search_results = []
           contex = {'search_results': search_results, 'query': query}
           return render(request, 'productapp_templates/search_result.html', contex)
       else:
           print('......')
           #search_results=Products.objects.annotate(search=SearchVector('name','description',)+SearchVector('plant_type','Sub_catagory_p',)+SearchVector('place_of_grown','maintanance','shape_for_candels_others','material_for_candels_others',)).filter(search=query)
           search_results=Products.objects.filter(description__search=query)
           print(search_results)
           contex = {'search_results': search_results, 'query': query}
           return render(request, 'productapp_templates/search_result.html', contex)
    else:
        return redirect('/')
 else:
     pass 

def add_to_cart(request):
    if request.method == 'POST':
      print('Post request is working ')
      user=request.user
      if user.is_authenticated:
        searched_id=request.POST['prod_custom_id_cart']
        print(searched_id)
        A=Cart.objects.filter(Q(product_p=searched_id) & Q(auth_user=user)) 
        print('Alll--------')
        if A:
           print("does not exist ..!")
           return redirect('PRODUCT:view_cart') 
        else:
          print("Is this gonna work or not ")
          user_now=request.user
          product_price_checker=Products.objects.filter(custom_id=searched_id)
          prod_id=Products.objects.get(custom_id=searched_id)
          print(product_price_checker)
          if product_price_checker:
           for i in product_price_checker:
            prod_verified_id=i.custom_id
            cart_total_price=i.off_price
            making_cart=Cart(auth_user=user_now,product_p=prod_id,cart_total=cart_total_price).save()
            print('product is saved to cart ')
          return redirect('PRODUCT:view_cart')
      else:
        return redirect('user_login')
    else:
      print("get request is working not the post one !")
      pass
@login_required(login_url='/user_login/')
def view_cart(request):
  if request.method =='GET':
     user_current=request.user
     total_amount=0
     final_amount=0
     temp_amount=0
     quantity=0
     check_cart=Cart.objects.filter(auth_user=user_current)
     if check_cart: 
       for p in check_cart: 
        quantity +=p.prod_quantity 
        temp_amount =float(p.prod_quantity)*float(p.product_p.off_price)  
        original_price_ofcart=p.cart_total  
        print('inside for loop so amount for each') 
        print(total_amount)   

       p.toal_payable_amount=total_amount+50    
       final_amount=total_amount+50   
       add=Address.objects.filter(user=user_current)  

       contex={'check_cart':check_cart,'original_price_ofcart':temp_amount,'total_amount':final_amount,'quantity':quantity,'no_object':'There is no object in the cart here !','add':add}
     
       return render(request,'productapp_templates/show_cart.html',contex)   

     return render (request,'productapp_templates/show_cart.html',{'no_product':'No Product is found please go to product page !'})  
  else:
     return redirect('view_cart')
    
def plus_cart(request):
    if request.method =='GET':
     prod_id=request.GET['prod_id']
     user_current=request.user
     print(prod_id)
     print('prod id is taken for adding more items in cart ')
     temp_amount=0
     total_amount=0
     final_amount=0
     cart_total_a=0
     quantity=0
     check_cart=Cart.objects.get(Q(product_p=prod_id) & Q(auth_user=user_current))
     check_cart.prod_quantity+=1
     check_cart.cart_total=check_cart.prod_quantity*check_cart.product_p.off_price
     check_cart.save()    
     #check_cart=[i for i in Cart.objects.all() if i.auth_user==user_current]
     check_cart=Cart.objects.filter(Q(product_p=prod_id) & Q(auth_user=user_current))
     if check_cart:
       for p in check_cart:
        quantity +=p.prod_quantity
        temp_amount =float(p.prod_quantity)*float(p.product_p.off_price)
        total_amount+=temp_amount
        cart_total_a+=p.cart_total
        print('inside for loop of plus cart feature ')
        print(total_amount) 
       final_amount=total_amount+50
       plus_cart_res={
         'check_cart':quantity,
         'total_amount':final_amount,
         'cart_total':cart_total_a,
         'T':temp_amount
         }
       print('json response has been sent to ajax!')
       return JsonResponse(plus_cart_res)
     return render (request,'productapp_templates/show_cart.html',{'no_product':'No Product is found please go to product page !'})    
    else:
      pass
def minus_cart(request):
 
  if request.method =='GET':
     prod_id=request.GET['prod_id']
     user_current=request.user
     print(prod_id)
     print('prod id is taken for adding more items in cart ')
     check_cart=Cart.objects.get(Q(product_p=prod_id) & Q(auth_user=user_current))
     check_cart.prod_quantity -=1
     check_cart.cart_total=check_cart.prod_quantity*check_cart.product_p.off_price
     if check_cart.prod_quantity <1 :
       check_cart.delete()
     else:
       check_cart.save()
     
     total_amount=0
     final_amount=0
     quantity=0

     check_cart=[i for i in Cart.objects.all() if i.auth_user==user_current]
     print(check_cart)
     if check_cart:
       for p in check_cart:
        quantity +=p.prod_quantity
        temp_amount =float(p.prod_quantity)*float(p.product_p.off_price)
        total_amount+=temp_amount
        print('inside for loop of plus cart feature ')
        print(total_amount) 
       final_amount=total_amount+50
       minus_cart_res={
         'check_cart':quantity,
         'total_amount':final_amount}
       print('json response has been sent to ajax!')
       return JsonResponse(minus_cart_res)
     return render (request,'productapp_templates/show_cart.html',{'no_product':'No Product is found please go to product page !'})
  else:
      pass
def remove_cart(request):
  if request.method =='GET':
     prod_id=request.GET['prod_id']
     user_current=request.user
     print(prod_id)
     print('This is to remove the product from cart.... ')
     check_cart=Cart.objects.get(Q(product_p=prod_id) & Q(auth_user=user_current))
     check_cart.delete()
     
     total_amount=0
     final_amount=0
     quantity=0

     check_cart=[i for i in Cart.objects.all() if i.auth_user==user_current]
     print(check_cart)
     if check_cart:
       for p in check_cart:
        quantity +=p.prod_quantity
        temp_amount =float(p.prod_quantity)*float(p.product_p.off_price)
        total_amount+=temp_amount
        print('inside for loop of plus cart feature ')
        print(total_amount) 
       final_amount=total_amount+50
       delete_cart_res={
         'check_cart':quantity,
         'total_amount':final_amount  }
       print('json response has been sent to ajax!')
       return JsonResponse(delete_cart_res)
     else:
       return render (request,'productapp_templates/show_cart.html',{'no_product':'No Product is found please go to product page !'})

  else:
      pass




def checkout(request):
 if request.method =='POST':
  try:   
    add_id=request.POST['check_add_id'] 
    print(add_id) 
    request.session['addressid']=add_id
    # name = request.POST.get('name')

    # print("razor has done")
    if add_id:
      user=request.user
      print(add_id)
      filter_add=Address.objects.get(Q(pk=add_id) & Q(user=user))
      user_current=request.user
      total_amount=0
      final_amount=0
      quantity=0
      
      print("So it's the id of particular product we want wwwe are on  -------Checkout  ")
      #filter_cart=Cart.objects.filter(auth_user=user_current)
      check_cart=Cart.objects.filter(auth_user=user_current) 
      print(check_cart)
      if check_cart: 
        for p in check_cart:
            prod_id_verified=p.product_p.custom_id
            print("-------")
            print(prod_id_verified)
            #request.session['order_prod_id']=prod_id
            quantity +=p.prod_quantity
            temp_amount =float(p.prod_quantity)*float(p.product_p.off_price)
            total_amount+=temp_amount
            prod_name=p.product_p.custom_id
            print(prod_name)
            print(total_amount) 
            id_for_ordermodel=Products.objects.get(custom_id=prod_id_verified)
            print("prod id verified ....")
            p.toal_payable_amount=total_amount+50
            final_amount=total_amount+50
            request.session['FinalAmount']=final_amount
            request.session['Quantity']=quantity
            tip=Tip.objects.filter(user=request.user).values()
            
            counter_tip=0
            amount_in_paisa=0
            if tip:
              request.session['Tip_session']=tip
              for i in tip:
                counter_tip=counter_tip+i.tips_count
              amount_in_paisa=amount_in_paisa+final_amount*100 +(counter_tip*20)*100
              request.session['paisa_amount']=amount_in_paisa
              print('order from checkout has been created')
              print(' So Mail has been sent to from checkout platform .... ')
              client = razorpay.Client(auth=('rzp_test_50rfJzBfpU9cKg','PgNnKwoydaq1EvyJeDhkFhF5'))
              print('crossed the client')
              payment = client.order.create({'amount': final_amount, 'currency': 'INR',
                                  'payment_capture': '1'})
              print('crossed the payment ')
              contex={'check_cart':check_cart,'T':total_amount,'total_amount':final_amount,'quantity':quantity,'filter_add':filter_add,'paisa':amount_in_paisa,'tip':tip}
              return render(request,'productapp_templates/checkout.html',contex)
     
            else:
              amount_in_paisa=final_amount*100 
              request.session['paisa_amount']=amount_in_paisa
              print('so there is no tip avilable for Waiter !')
            
              client = razorpay.Client(
              auth=('rzp_test_50rfJzBfpU9cKg','PgNnKwoydaq1EvyJeDhkFhF5'))
              payment = client.order.create({'amount': final_amount, 'currency': 'INR',
                                  'payment_capture': '1'})
              print("Error on last line ")
              contex={'check_cart':check_cart,'T':total_amount,'total_amount':final_amount,'quantity':quantity,'filter_add':filter_add,'paisa':amount_in_paisa}
            # Order(customer_name=user,o_palced_name=id_for_ordermodel,user_address=filter_add,order_price=final_amount,order_quantity=quantity).save()
            #cart.delete()
                    
        #  del request.session['order_prod_id']
        contex={'check_cart':check_cart,'T':total_amount,'total_amount':final_amount,'quantity':quantity,'filter_add':filter_add,'paisa':amount_in_paisa,'tip':tip}
        #order_create=Order()

        return render(request,'productapp_templates/checkout.html',contex)
        
    
    
      return render (request,'productapp_templates/checkout.html',{'no_product':'Nothing to check out go for shopping !'})  
  
    else:
      return render (request,'productapp_templates/checkout.html',{'no_add':'Nothing to check out go for shopping !'})  
  except Exception as e:
    print('except block is running ')
    print(e)
    return redirect('/add_address/')
 else:
    return redirect('/')



###################               TIP COIN     ########################
def add_tipcoin(request):
    print("get request on add_tipcoin")
    total_coin=0
    coin_number=request.GET['prod_id']
    prod_id=request.session.get('addressid')
    tip_checker=Tip.objects.filter(user=request.user)
    if tip_checker:
        for i in tip_checker:
            print(i.tips_count)
            i.tips_count=i.tips_count+1
            i.save()
        print("Done saving th added coin ") 
        return JsonResponse({'key':'key'})
    else:
      coin_number_new=1
      print("created the tip coin ")
      Tip(user=request.user,tips_count=coin_number_new).save()
          
      return JsonResponse({'key_name':'done here !'})
def reduce_tipcoin(request):
    coin_number=request.GET['prod_id']
    tip_checker=Tip.objects.filter(user=request.user)
    if tip_checker:
      for i in tip_checker:
        i.tips_count=i.tips_count-1
        i.save()
      return JsonResponse({'key':'key'})
    else:
      pass 
    

  #######################   ADDRESSSS      #########################

def add_address(request):
  if request.method=='POST':
      
    f_add=request.POST['full_address']
    pin=request.POST['pin']
    ph_no=request.POST['1st_phone']
    p=Address(user=request.user,f_add=f_add,pin=pin,ph_no=ph_no).save()
    return redirect('/add_address/')
  else:
    p=Address.objects.filter(user=request.user)
    return render(request,'productapp_templates/add_address.html',{'p':p})


def payment_done(request):
   if request.method=='POST':
    user=request.user
    check_cart=Cart.objects.filter(auth_user=user)
    add_id=request.session.get('addressid')
    #final_amount=request.session.get('FinalAmount')
    checker=request.session.get('paisa_amount')
    final_amount=checker/100
    tip_number=request.session.get('Tip_session') or 0

    check_add=Address.objects.get(Q(pk=add_id) & Q(user=user))
    for p in check_cart:
     prod_id_verified=p.product_p.custom_id
     prod_name=p.product_p
     #final_amount=request.session.get('FinalAmount')
     checker=request.session.get('paisa_amount')
     final_amount=checker/100
     quantity=request.session.get('Quantity')
     Order(customer_name=user,o_palced_name=prod_name,user_address=check_add,order_price=final_amount,order_quantity=quantity,tip_coin=tip_number).save()
     check_cart.delete()
     del request.session['paisa_amount']
     del request.session['addressid']
        #del request.session['Tip_session']
     print('data deleted!')
     message=f"order has been created from {user}, amount paid ={final_amount}---- and Full address will be shown in database ==== {check_add}"
     send_mail(
                'New Order',
                message,
                'foundationssaksham@gmail.com',
                ['jokesprogramming@gmail.com'],
                fail_silently=False,)
     print(' So Mail has been sent from payment done ... ')
     try:
       del request.session['Tip_session']
       return redirect('/dashboard/')
     except:
       return redirect('/dashboard/')
   else:
    pass

   return render(request,'productapp_templates/payment_done.html')