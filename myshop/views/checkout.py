from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from django.views import View
from myshop.models.product import Product
from myshop.models.orders import Order
from myshop.models import Customer


class CheckOut(View):

    def get(self, request):
        return redirect('cart')

    def post(self, request):
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer = request.session.get('customer')
        cart = request.session.get('cart')
        products = Product.get_products_by_id(list(cart.keys()))
        print(address,phone,customer,cart,products)
        
        if customer:
            for product in products:
                order = Order(customer = Customer(id=customer),
                            product = product,
                            price = product.price,
                            address = address,
                            phone = phone,
                            quantity = cart.get(str(product.id)))
                order.save()
                request.session['cart'] = {}
        else:
            returnUrl = request.META['PATH_INFO']
            print(returnUrl)
            return redirect(f'/customer_login?next={returnUrl}')

        return redirect('index') 
