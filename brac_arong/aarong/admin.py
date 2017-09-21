from django.contrib import admin

from aarong.models import Category, SaleProductList
from aarong.models import Product
# Register your models here.
from aarong.models import Route
from aarong.models import Sale
from aarong.models import Shop

admin.site.register(Route)
admin.site.register(Shop)
admin.site.register(Sale)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(SaleProductList)