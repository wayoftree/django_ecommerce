from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect
from django.views import View
from myshop.models.customer import Customer


class CustomerLogin(View):

    def get(self, request):
        return render(request, 'customer_login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.get_customer_by_email(email)
        error_message = None
        if customer:
            flag = check_password(password, customer.password)
            if flag:
                # request.session['customer_id'] = customer.id
                # request.session['email'] = customer.email
                request.session['customer'] = customer.id
                return redirect('index')
            else:
                error_message = 'Email or Password Invalid !!'
        else:
            error_message = 'Email or Password Invalid !!'

        print(customer)
        print(password)
        return render(request, 'customer_login.html', {'error': error_message})


def logout(request):
    request.session.clear()
    return redirect('customer_login')