from django.db import models
from decimal import Decimal, ROUND_HALF_UP
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.conf import settings
import os
from accounts.models import CustomUser

class Color(models.Model):
    color_id = models.CharField(max_length=4, blank=True)
    name = models.CharField(max_length=255, unique=True)
    hex_code = models.CharField(max_length=7, unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.color_id:
            last_id = Color.objects.order_by('-id').first()
            if last_id:
                new_id = str(int(last_id.id) + 1).zfill(4)
            else:
                new_id = '0001'
            self.color_id = new_id

        self.hex_code = self.hex_code.upper()

        super().save(*args, **kwargs)


class Category(models.Model):
    category_id = models.CharField(max_length=4, blank=True)
    name = models.CharField(max_length=50)
    
    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        if not self.category_id:
            last_id = Category.objects.order_by('-id').first()
            if last_id:
                new_id = str(int(last_id.id) + 1).zfill(4)
            else:
                new_id = '0001'
            self.category_id = new_id
        super().save(*args, **kwargs)

class Product(models.Model):
    DISCOUNT_TYPE_CHOICES = [
        ('percentage', 'Percentage'),
        ('amount', 'Amount'),
        ('none', 'None'),
    ]

    product_id = models.CharField(max_length=8, unique=True, blank=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_type = models.CharField(max_length=10, choices=DISCOUNT_TYPE_CHOICES, default='none')
    discount_value = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True)
    multiple_colors = models.BooleanField(default=False)
    colors = models.ManyToManyField(Color, related_name='colors')
    image = models.ImageField()
    categories = models.ManyToManyField(Category, related_name='categories')
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def final_price(self):
        if self.discount_type == 'percentage':
            discount_amount = (self.discount_value / 100) * self.price
            final_price = self.price - discount_amount
        elif self.discount_type == 'amount':
            final_price = self.price - self.discount_value
        else:
            final_price = self.price

        return Decimal(final_price).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)

    def comments(self):
        return self.comment_set.all()

    def rating_average(self):
        comments = self.comment_set.all()
        if comments:
            total_rating = sum(comment.rating for comment in comments)
            return total_rating / len(comments)
        else:
            return 0.0

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.product_id:
            last_id = Product.objects.order_by('-id').first()
            if last_id:
                new_id = str(int(last_id.id) + 1).zfill(8)
            else:
                new_id = '00000001'
            self.product_id = new_id
        super().save(*args, **kwargs)


class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    rating = models.FloatField(default=0)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.product.name}"

class FollowImage(models.Model):
    follow_image_id = models.CharField(max_length=1, unique=True, blank=True)
    image_data = models.BinaryField()

    def __str__(self):
        return self.follow_image_id

    def save(self, *args, **kwargs):
        if not self.follow_image_id:
            last_id = FollowImage.objects.order_by('-id').first()
            if last_id:
                new_id = str(int(last_id.id) + 1)
            else:
                new_id = '1'
            self.follow_image_id = new_id

        # Convert the image file to bytes and save it in the database
        if self.image:
            self.image_data = self.image.read()

        super().save(*args, **kwargs)



class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    items = models.ManyToManyField('CartItem')
    
    def __str__(self):
        return f"Cart for {self.user.username}"


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def subtotal(self):
        return self.product.final_price * self.quantity

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.user.username

