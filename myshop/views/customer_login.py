from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.views import View
from myshop.models.customer import Customer


class CustomerLogin(View):

    next = None

    def get(self, request):
        CustomerLogin.next = request.GET.get('next')
        if request.session.get('customer'):
            return redirect('index')
        else:
            return render(request, 'customer_login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.get_customer_by_email(email)
        error_message = None
        if customer:
            flag = check_password(password, customer.password)
            if flag:
                request.session['customer'] = customer.id
                if CustomerLogin.next:
                    return HttpResponseRedirect(CustomerLogin.next)
                else:
                    CustomerLogin.next = None
                    redirect('index')
            else:
                error_message = 'Email or Password Invalid !!'
        else:
            error_message = 'Email or Password Invalid !!'

        print(customer)
        print(password)
        return render(request, 'customer_login.html', {'error': error_message})


def logout(request):
    request.session.clear()
    return redirect('index')