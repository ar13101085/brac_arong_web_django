from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from django.utils.timezone import now

class AppUser(models.Model):
    user=models.OneToOneField(User);
    picture=models.ImageField();
    class Meta:
        verbose_name = 'Aarong User'
        verbose_name_plural = 'Aarong Users'
    def __str__(self):
        return self.user.email;


class Category(models.Model):
    CategoryId = models.AutoField(primary_key=True);
    CategoryName=models.CharField(max_length=200,default="");
    CategoryPhoto=models.ImageField(null=True)
    class Meta:
        verbose_name = 'Product Category'
        verbose_name_plural = 'Product Category'
    #list product
    def __str__(self):
        return str(self.CategoryId)+" "+self.CategoryName;

class Product(models.Model):
    ProductId= models.AutoField(primary_key=True);
    ProductName=models.CharField(max_length=200,default="");
    ProductUnitPrice=models.FloatField(default=0)
    Category=models.ForeignKey(Category,blank=False)
    ProductPhoto=models.ImageField(null=True)
    class Meta:
        verbose_name = 'Aarong Product'
        verbose_name_plural = 'Aarong Products'
    def __str__(self):
        return str(self.ProductId)+" "+self.ProductName+" "+self.Category.CategoryName;
class Area(models.Model):
    id=models.AutoField(primary_key=True);
    areaName=models.CharField(max_length=200,default="");
    class Meta:
        verbose_name = 'Area'
        verbose_name_plural = 'Area'
    def __str__(self):
        return str(self.id)+" "+self.areaName;
class Branch(models.Model):
    id = models.AutoField(primary_key=True);
    branchName=models.CharField(max_length=200,default="");
    User = models.OneToOneField(User, blank=True)
    Area = models.ForeignKey(Area, blank=True)  # route must have a branch
    class Meta:
        verbose_name = 'Branch'
        verbose_name_plural = 'Branch'
    def __str__(self):
        return str(self.id)+" "+self.branchName;

class Route(models.Model):
    RouteId=models.AutoField(primary_key=True);
    RouteName=models.CharField(max_length=200,default="");
    Branch=models.ForeignKey(Branch, blank=True)  # route must have a branch
    #list of all shop
    class Meta:
        verbose_name = 'Route'
        verbose_name_plural = 'Route'
    def __str__(self):
        return str(self.RouteId)+" "+self.RouteName;

class Shop(models.Model):
    ShopId=models.AutoField(primary_key=True);
    ShopLat=models.FloatField(default=0.0);
    ShopLng=models.FloatField(default=0.0);
    ShopProviderName=models.CharField(max_length=200,default="");
    ShopGpsAddress=models.CharField(max_length=200,default="");
    ShopDetailsAddress=models.CharField(max_length=200,default="");
    ShopCreatedTime=models.DateTimeField(auto_now=True, blank=True)
    Route=models.ForeignKey(Route,blank=False)
    ShopPhoto=models.ImageField(null=True)
    class Meta:
        verbose_name = 'Shop'
        verbose_name_plural = 'Shop'
    def __str__(self):
        return str(self.ShopId)+" "+self.ShopProviderName;


class Sale(models.Model):
    SaleId = models.AutoField(primary_key=True);
    Shop = models.ForeignKey(Shop,blank=False,default=None);
    OrderCreatedTime = models.DateTimeField(auto_now=True, blank=True);
    Total = models.FloatField(default=0.0);
    User = models.ForeignKey(User, blank=False,default=None)

    class Meta:
        verbose_name = 'Sale History'
        verbose_name_plural = 'Sale History'
    def __str__(self):
        return str(self.SaleId)+" "+str(self.Shop.ShopProviderName);

class SaleProductList(models.Model):
    id=models.AutoField(primary_key=True);
    Product = models.ForeignKey(Product, default=None)
    Sale=models.ForeignKey(Sale,default=None);
    saleQuantity = models.IntegerField(default=0);
    saleMoney=models.FloatField(default=0.0);
    CreatedTime = models.DateField(default=now);
    class Meta:
        verbose_name = 'Sale Product History'
        verbose_name_plural = 'Sale Product History'
    def __str__(self):
        return self.Product.Category.CategoryName+" "+self.Product.ProductName+" "+str(self.saleMoney);

class OtherVendor(models.Model):
    id = models.AutoField(primary_key=True);
    name=models.CharField(max_length=100,default='');
    class Meta:
        verbose_name = 'Other vendor information'
        verbose_name_plural = 'Other vendor information'
    def __str__(self):
        return str(self.id)+" "+self.name;
class OtherVendorSaleProduct(models.Model):
    id = models.AutoField(primary_key=True);
    Category = models.ForeignKey(Category,related_name="category_name")
    CreatedTime = models.DateField(default=now);
    Unit = models.IntegerField(default=0);
    saleMoney = models.FloatField(default=0.0);
    VendorName=models.ForeignKey(OtherVendor,blank=False,related_name="other_vendor");
    class Meta:
        verbose_name = 'Other vendor sale history'
        verbose_name_plural = 'Other vendor sale history'
    def __str__(self):
        return str(self.id)+" "+self.Category.CategoryName+" "+str(self.CreatedTime);

class Notification(models.Model):
    id = models.AutoField(primary_key=True);
    title=models.TextField(default="");
    text=models.TextField(default="");
    CreatedTime = models.DateTimeField(auto_now=True, blank=True);
    class Meta:
        verbose_name = 'Reward'
        verbose_name_plural = 'Reward'
    def __str__(self):
        return str(self.id)+" "+self.title;
class NiceColor(models.Model):
    id=models.AutoField(primary_key=True);
    code=models.CharField(max_length=10);
    def __str__(self):
        return str(self.id)+"       "+self.code;