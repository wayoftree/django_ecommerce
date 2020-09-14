from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render, redirect
from .models import Seller
from myshop.models.product import Product
from myshop.models.category import Category
import os


# Create your views here.


def seller_login(request):
    if request.session.get('seller'):
        return redirect('dashboard')
    else:
        if request.method == 'GET':
            return render(request, 'seller_login.html')
        else:
            email = request.POST.get('email')
            password = request.POST.get('password')
            seller = Seller.get_seller_by_email(email)
            error_message = None
            if seller:
                flag = check_password(password, seller.password)
                if flag:
                    request.session['seller'] = seller.id
                    return redirect('dashboard')
                else:
                    error_message = 'Email or Password Invalid !!'
            else:
                error_message = 'Email or Password Invalid !!'

            return render(request, 'seller_login.html', {'error': error_message})


def seller_signup(request):
    if request.method == "GET":
        return render(request, 'seller_signup.html')
    else:
        postData = request.POST
        first_name = postData.get('firstname')
        last_name = postData.get('lastname')
        phone = postData.get('phone')
        email = postData.get('email')
        password = postData.get('password')
        firm_name = postData.get('firm_name')
        business_no = postData.get('business_no')
        office_address = postData.get('office_address')
        state = postData.get('state')
        city = postData.get('city')

        # Hold Previous Input

        value = {
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'email': email,
            'firm_name': firm_name,
            'business_no': business_no,
            'office_address': office_address,
            'state': state,
            'city': city,
        }

        error_message = None

        seller = Seller(first_name=first_name,
                        last_name=last_name,
                        phone=phone,
                        email=email,
                        password=password,
                        firm_name=firm_name,
                        business_no=business_no,
                        office_address=office_address,
                        state=state,
                        city=city)

        error_message = validateCustomer(seller)

        # saving data to database

        if not error_message:
            print(first_name, last_name, phone, email, password)
            seller.password = make_password(seller.password)
            seller.register()
            return redirect('index')
        else:
            data = {
                'error': error_message,
                'values': value
            }
            return render(request, 'seller_signup.html', data)


def validateCustomer(seller):
    error_message = None
    if not seller.first_name:
        error_message = "First Name Required !!"
    elif len(seller.first_name) < 3:
        error_message = 'First Name must be 3 char long or more'
    elif not seller.last_name:
        error_message = 'Last Name Required'
    elif len(seller.last_name) < 3:
        error_message = 'Last Name must be 3 char long or more'
    elif not seller.phone:
        error_message = 'Phone Number required'
    elif len(seller.phone) < 10:
        error_message = 'Phone Number must be 10 char Long'
    elif len(seller.password) < 6:
        error_message = 'Password must be 6 char long'
    elif len(seller.email) < 5:
        error_message = 'Email must be 5 char long'
    elif not seller.office_address:
        error_message = 'Office Address required'
    elif not seller.firm_name:
        error_message = 'Company or Firm name required'
    elif not seller.business_no:
        error_message = 'Company or Firm name required'
    elif not seller.state:
        error_message = 'State required'
    elif not seller.city:
        error_message = 'City required'
    elif seller.isExists():
        error_message = 'Email Address or Phone Number Already Registered..'

    return error_message


def dashboard(request):
    if request.session.get('seller'):
        if request.method == 'GET':
            seller_id = request.session.get('seller')
            if seller_id:
                print(seller_id)
                products = Product.get_seller_product_by_id(seller_id)
                return render(request, 'seller_dashboard.html', {'products': products})
    else:
        return redirect('seller_login')


def add_product(request):
    if request.session.get('seller'):
        if request.method == "GET":
            category = Category.get_all_categories()
            return render(request, 'add_product.html', {'category': category})
        else:
            postData = request.POST
            name = postData.get('name')
            price = postData.get('price')
            category_id = postData.get('category_id')
            seller_id = postData.get('seller_id')
            description = postData.get('description')
            image = request.FILES['image']

            category = Category.objects.get(id=category_id)

            seller = Seller.objects.get(id=seller_id)

            product = Product(name=name,
                              price=price,
                              category=category,
                              seller=seller,
                              description=description,
                              image=image,
                              )
            product.product_register()
            return redirect('dashboard')
    else:
        return redirect('seller_login')


def edit_product(request, cid):
    if request.session.get('seller'):
        if request.method == 'GET':
            product = Product.objects.filter(id=cid)
            category = Category.get_all_categories()
            print(product, category)
            data = {'products': product, 'category': category}
            return render(request, 'edit_product.html', data)
        else:
            postData = request.POST
            name = postData.get('name')
            price = postData.get('price')
            category_id = postData.get('category_id')
            # seller_id = postData.get('seller_id')
            description = postData.get('description')
            image = request.FILES.get('image', False)
            if not image:
                Product.objects.filter(id=cid).update(name=name, price=price, category_id=category_id,
                                                      description=description)
            else:
                base_dir = r'uploads/products'
                filename = str(image)
                path = os.path.join(base_dir, filename)
                Product.objects.filter(id=cid).update(name=name, price=price, category_id=category_id,
                                                      description=description,
                                                      image=path)

            return redirect('dashboard')
    else:
        return redirect('seller_login')


def delete_product(request, cid):
    if request.session.get('seller'):
        b = Product.objects.filter(id=cid)
        b.delete()
        return redirect('dashboard')
    else:
        return redirect('seller_login')
