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
admin.site.register(OtherVendorSaleProduct,OtherVendorSaleProductAdmin)

class SaleProductListProductAdmin(admin.ModelAdmin):
    list_display=('id','Product','saleQuantity','saleMoney','CreatedTime');
admin.site.register(SaleProductList,SaleProductListProductAdmin)

class RouteAdmin(admin.ModelAdmin):
    list_display=('RouteId','RouteName','Branch');
admin.site.register(Route,RouteAdmin)



class ShopAdmin(admin.ModelAdmin):
    list_display=('ShopId','ShopLat','ShopLng','ShopProviderName','ShopGpsAddress','ShopDetailsAddress','ShopCreatedTime','Route','ShopPhoto');
admin.site.register(Shop,ShopAdmin)



class SaleAdmin(admin.ModelAdmin):
    list_display=('SaleId','Shop','OrderCreatedTime','Total','User');
admin.site.register(Sale,SaleAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display=('CategoryId','CategoryName','CategoryPhoto');
admin.site.register(Category,CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display=('ProductId','ProductName','ProductUnitPrice',"Category",'ProductPhoto');
admin.site.register(Product,ProductAdmin)


class OtherVendorAdmin(admin.ModelAdmin):
    list_display=('id','name');
admin.site.register(OtherVendor,OtherVendorAdmin)

class NotificationAdmin(admin.ModelAdmin):
    list_display=('id','title','text','CreatedTime');
admin.site.register(Notification,NotificationAdmin)

class AppUserAdmin(admin.ModelAdmin):
    list_display=('user','picture');
admin.site.register(AppUser,AppUserAdmin)


admin.site.register(NiceColor)

class AreaAdmin(admin.ModelAdmin):
    list_display=('id','areaName');
admin.site.register(Area,AreaAdmin)


class BranchAdmin(admin.ModelAdmin):
    list_display=('id','branchName','User','Area');
admin.site.register(Branch,BranchAdmin)