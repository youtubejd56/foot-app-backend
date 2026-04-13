from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
     user = models.OneToOneField(User, on_delete=models.CASCADE)
     phone = models.CharField(max_length=15, blank=True)
     address = models.TextField(blank=True)
     city = models.CharField(max_length=100, blank=True)
     zip_code = models.CharField(max_length=10, blank=True)

     def __str__(self):
         return f"{self.user.username}'s Profile"

class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    rating = models.FloatField(default=4.0)
    delivery_time = models.CharField(max_length=50, default="30-40 min")
    price_for_two = models.CharField(max_length=100, default="₹500 for two")
    category = models.CharField(max_length=100, default="Mixed")
    image_url = models.URLField(max_length=500, blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    offers = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    items_count = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default="Pending")

    def __str__(self):
        return f"Order #{self.id} - {self.status}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    restaurant_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
