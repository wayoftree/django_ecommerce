from django.urls import path
from .views import home, customer_login, customer_signup, cart, checkout, orders
from myshop.middlewares.auth import simple_middleware


urlpatterns = [
	path('', home.Index.as_view(), name="index"),
	path('customer_signup/', customer_signup.CustomerSignup.as_view(), name="customer_signup"),
	path('customer_login/', customer_login.CustomerLogin.as_view(), name="customer_login"),
	path('logout/', customer_login.logout, name="logout"),
	path('cart/', cart.Cart.as_view(), name="cart"),
	path('checkout/', checkout.CheckOut.as_view(), name="checkout"),
	path('orders/', simple_middleware(orders.OrderView.as_view()), name="orders"),

]