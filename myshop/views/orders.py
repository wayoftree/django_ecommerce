from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from django.views import View
from myshop.models.customer import Customer
from myshop.models.product import Product
from myshop.models.orders import Order
from myshop.middlewares.auth import simple_middleware
from django.utils.decorators import method_decorator


class OrderView(View):

    @method_decorator(simple_middleware)
    def get(self, request):
        customer = request.session.get('customer')
        orders = Order.get_orders_by_customer(customer)
        #print(orders)
        return render(request, 'orders.html', {'orders': orders})
