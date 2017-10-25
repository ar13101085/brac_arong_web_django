from django.contrib import admin

from aarong.models import Category, SaleProductList, OtherVendor, OtherVendorSaleProduct, Notification, AppUser, \
    NiceColor, Area, Branch
from aarong.models import Product
# Register your models here.
from aarong.models import Route
from aarong.models import Sale
from aarong.models import Shop

class OtherVendorSaleProductAdmin(admin.ModelAdmin):
    list_display=('id','Category','CreatedTime','Unit','saleMoney','VendorName');


admin.site.register(Route)
admin.site.register(Shop)
admin.site.register(Sale)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(SaleProductList)


admin.site.register(OtherVendor)
admin.site.register(OtherVendorSaleProduct,OtherVendorSaleProductAdmin)
admin.site.register(Notification)
admin.site.register(AppUser)
admin.site.register(NiceColor)

admin.site.register(Area)
admin.site.register(Branch)