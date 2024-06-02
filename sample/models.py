# from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.contrib.auth import get_user_model
from django.conf import settings


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, verbose_name="メールアドレス")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    
    
class Category(models.Model):
    name = models.CharField(max_length=100)    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

    

class Item(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    release_date = models.DateField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE,null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    purchased = models.BooleanField(default=False)  # 購入済みフラグを追加

    
class Favorite(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    items = models.ManyToManyField(Item, blank=True)  # 多対多の関係を設定
    name = models.CharField(max_length=100, default='仮名')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Share(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    owner_user = models.ForeignKey(CustomUser, related_name='owner_user', on_delete=models.CASCADE)
    shared_with_user = models.ForeignKey(CustomUser, related_name='shared_with_user', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Budget(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    favorite = models.ForeignKey(Favorite, on_delete=models.CASCADE, null=True, blank=True)
    month = models.DateField()
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
