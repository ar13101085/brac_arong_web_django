from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Category(models.Model):
    CategoryId = models.AutoField(primary_key=True);
    CategoryName=models.CharField(max_length=200,default="");
    CategoryPhoto=models.ImageField(null=True)
    #list product
    def __str__(self):
        return str(self.CategoryId)+" "+self.CategoryName;

class Product(models.Model):
    ProductId= models.AutoField(primary_key=True);
    ProductName=models.CharField(max_length=200,default="");
    ProductUnitPrice=models.FloatField(default=0)
    Category=models.ForeignKey(Category,blank=False)
    ProductPhoto=models.ImageField(null=True)
    def __str__(self):
        return str(self.ProductId)+" "+self.ProductName+" "+self.Category.CategoryName;


class Route(models.Model):
    RouteId=models.AutoField(primary_key=True);
    RouteName=models.CharField(max_length=200,default="");
    RouteLat=models.FloatField(default=0.0);
    RouteLng=models.FloatField(default=0.0);
    User=models.ForeignKey(User,blank=True) # route must have a user
    #list of all shop
    def __str__(self):
        return str(self.RouteId)+" "+self.RouteName;

class Shop(models.Model):
    ShopId=models.AutoField(primary_key=True);
    ShopLat=models.FloatField(default=0.0);
    ShopLng=models.FloatField(default=0.0);
    ShopProviderName=models.CharField(max_length=200,default="");
    ShopGpsAddress=models.CharField(max_length=200,default="");
    ShopDetailsAddress=models.CharField(max_length=200,default="");
    ShopCreatedTime=models.DateTimeField(auto_now_add=True, blank=True)
    Route=models.ForeignKey(Route,blank=False)
    ShopPhoto=models.ImageField(null=True)
    def __str__(self):
        return str(self.ShopId)+" "+self.ShopProviderName;


class Sale(models.Model):
    SaleId = models.AutoField(primary_key=True);
    Shop = models.ForeignKey(Shop,blank=False,default=None);
    OrderCreatedTime = models.DateTimeField(auto_now_add=True, blank=True);
    Total = models.FloatField(default=0.0);
    User = models.ForeignKey(User, blank=False,default=None)

    def __str__(self):
        return str(self.SaleId)+" "+str(self.Shop.ShopProviderName);

class SaleProductList(models.Model):
    id=models.AutoField(primary_key=True);
    Product = models.ForeignKey(Product, default=None)
    Sale=models.ForeignKey(Sale,default=None);
    saleQuantity = models.IntegerField(default=0);
    saleMoney=models.FloatField(default=0.0);

