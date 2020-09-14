from django.db import models
from .category import Category
from seller.models.seller import Seller


class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, default=1)
    description = models.CharField(max_length=200, default='')
    image = models.ImageField(upload_to='uploads/products/')

    def product_register(self):
        self.save()

    @staticmethod
    def get_products_by_id(ids):
        return Product.objects.filter(id__in =ids)
        
    @staticmethod
    def get_all_products():
        return Product.objects.all()

    @staticmethod
    def get_all_products_by_categoryid(category_id):
        if category_id:
            return Product.objects.filter(category=category_id)
        else:
            return Product.get_all_products()

    # Getting product to seller dashboard
    @staticmethod
    def get_seller_product_by_id(seller_id):
        try:
            return Product.objects.filter(seller_id=seller_id)
        except:
            return False

    def __str__(self):
        return self.name