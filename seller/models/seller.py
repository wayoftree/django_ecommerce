from django.db import models


class Seller(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    password = models.CharField(max_length=500)
    firm_name = models.CharField(max_length=200)
    business_no = models.CharField(max_length=100)
    office_address = models.CharField(max_length=300)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)

    def register(self):
        self.save()

    def isExists(self):
        if Seller.objects.filter(email=self.email) or Seller.objects.filter(phone=self.phone):
            return True

        return False

    @staticmethod
    def get_seller_by_email(email):
        try:
            return Seller.objects.get(email=email)
        except:
            return False
