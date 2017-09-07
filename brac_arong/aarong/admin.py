from django.contrib import admin

# Register your models here.
from aarong.models import Route
from aarong.models import Shop
from aarong.models import Order
from aarong.models import Sale
from aarong.models import Category
from aarong.models import Product

admin.site.register(Route)
admin.site.register(Shop)
admin.site.register(Order)
admin.site.register(Sale)
admin.site.register(Category)
admin.site.register(Product)