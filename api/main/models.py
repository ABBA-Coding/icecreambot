from django.contrib.auth.models import AbstractBaseUser
from .managers import CustomUserManager
from ordered_model.models import OrderedModel
from django.db import models


class Category(models.Model):
    name_uz = models.CharField(max_length=100)
    name_ru = models.CharField(max_length=100, blank=True, null=True)
    name_en = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name_uz


class Product(OrderedModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    price = models.IntegerField()
    photo = models.ImageField()
    name_uz = models.CharField(max_length=100)
    name_ru = models.CharField(max_length=100, blank=True, null=True)
    name_en = models.CharField(max_length=100, blank=True, null=True)
    photo_uri = models.CharField(max_length=255, blank=True, null=True)
    photo_updated = models.BooleanField(default=False)
    massa = models.IntegerField(default=105)
    jirnost = models.IntegerField(default=15)
    temperature = models.IntegerField(default=18)
    srok_godnosti = models.IntegerField(default=18, help_text="Указывается в месяцах")
    upakovka = models.CharField(max_length=15, default="Флоу-Пак")
    protein = models.FloatField(default=3.7)
    fat = models.FloatField(default=14.4)
    carbohydrate = models.FloatField(default=24.2)
    calories = models.IntegerField(default=1008)

    order_with_respect_to = "category"

    def __str__(self):
        return self.name_uz

    def save(self, *args, **kwargs):
        # Check if the photo field has changed
        if self.pk is not None:
            original_photo = Product.objects.get(pk=self.pk).photo
            if original_photo and original_photo != self.photo:
                self.photo_updated = True

        super(Product, self).save(*args, **kwargs)


class CustomUser(AbstractBaseUser):
    id = models.PositiveBigIntegerField(primary_key=True)  # Using ID as primary key
    username = models.CharField(max_length=150, null=True)
    fullname = models.CharField(max_length=255)
    user_lang = models.CharField(max_length=2, default='uz')

    is_admin = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'id'  # Using ID as the authentication field
    REQUIRED_FIELDS = ['fullname']  # Other required fields for creating a user

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    @property
    def is_staff(self):
        return self.is_admin

    def __str__(self):
        return str(self.id)


class UserLocations(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="locations")
    longitude = models.FloatField()
    latitude = models.FloatField()
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
