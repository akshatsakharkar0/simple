from django.db import models
from django.contrib.auth.models import User

# Category choices
CATEGORY_CHOICES = [
    ('turmeric', 'Turmeric'),
    ('chilli', 'Chilli'),
    ('coriander', 'Coriander'),
    ('biomass', 'BioMass'),
]

# Location choices
LOCATION_CHOICES = [
    ('all_over_the_world', 'All Over The World'),
    ('only_in_india', 'Only In India'),
]

class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.CharField(max_length=20, choices=[('coming_soon', 'Coming Soon'),
                                                     ('in_stock', 'In Stock'),
                                                     ('out_of_stock', 'Out Of Stock')])
    location = models.CharField(max_length=50, choices=LOCATION_CHOICES)
    image = models.ImageField(upload_to='item_images/', blank=True, null=True)

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Cart of {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    size_in_kg = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.item.name} - {self.quantity} x {self.size_in_kg}kg"


