import json

from django.http import HttpResponse
from django.shortcuts import render
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict

from aarong.models import Product, Category, Shop, Route


def GetAllShopInRoute(request):
    route=Route.objects.get(pk=request.GET.get('id'))
    allShop=Shop.objects.filter(Route=route).all();

    shops=[];
    for x in allShop:
        shop=model_to_dict(x);
        if x.ShopPhoto:
            shop['ShopPhoto']=x.ShopPhoto.url;
        else:
            shop['ShopPhoto'] ='';
        shops.append(shop);
    return HttpResponse(json.dumps(shops), content_type='json');

def GetAllRoute(request):
    routeList=Route.objects.all();
    routes=[];
    for x in routeList:
        routes.append(model_to_dict(x));
    return HttpResponse(json.dumps(routes), content_type='json');

def GetAllProduct(request):
    # productList = Product.objects.all().select_related();
    # productData = [];
    # for data in productList:
    #     x = {};
    #     x['ProductId'] = data.ProductId;
    #     x['ProductName'] = data.ProductName;
    #     x['ProductUnitPrice'] = data.ProductUnitPrice;
    #     if data.ProductPhoto:
    #         x['ProductPhoto'] = data.ProductPhoto.url;
    #     else:
    #         x['ProductPhoto'] = '';
    #     x['category'] = {};
    #     category = Category.objects.get(pk=data.Category_id);
    #     x['category'] = {'id': category.CategoryId, 'name': category.CategoryName};
    #     productData.append(x)
    # return HttpResponse(json.dumps(productData), content_type='json');
    shopId=request.GET.get('shopId');# next time use for suggetion product
    print("shop id is "+str(shopId));
    allCategory=Category.objects.all();
    all=[];
    for x in allCategory:
        data={};
        data['CategoryId']=x.CategoryId;
        data['CategoryName']=x.CategoryName;
        if x.CategoryPhoto:
            data['CategoryPhoto']=x.CategoryPhoto.url;
        else:
            data['CategoryPhoto']='';
        data['ProductList']=[];
        categoryProduct=Product.objects.filter(Category=x).all();
        for y in categoryProduct:
            product={};
            product['ProductId']=y.ProductId;
            product['ProductName']=y.ProductName;
            product['ProductUnitPrice']=y.ProductUnitPrice;
            if y.ProductPhoto:
                product['ProductPhoto']=y.ProductPhoto.url;
            else:
                product['ProductPhoto']='';
            data['ProductList'].append(product);
        all.append(data);

    return HttpResponse(json.dumps(all), content_type='json');
@csrf_exempt
def AddShop(request):
    route = Route.objects.get(pk=request.POST['RouteId']);
    res={};
    if route:
        shop = Shop(ShopLat=request.POST['ShopLat'], ShopLng=request.POST['ShopLng'],
                    ShopProviderName=request.POST['ShopProviderName'], ShopGpsAddress=request.POST['ShopGpsAddress'],
                    ShopDetailsAddress=request.POST['ShopDetailsAddress'],
                    Route=route, ShopPhoto=request.FILES['ShopPhoto']);
        shop.save();
        newShop=model_to_dict(shop);
        newShop['ShopPhoto']=newShop['ShopPhoto'].url;
        res={'res':True,'msg':'successfully add shop','shop':newShop};
        return HttpResponse(json.dumps(res), content_type='json');
    else:
        res = {'res': False, 'msg': 'no route id found', 'shop': {}};
        return HttpResponse(json.dumps(res), content_type='json');
@csrf_exempt
def SaleAdd(request):
    print(json.loads(str(request.POST.getlist('Sales'))));
    return HttpResponse(json.dumps({}), content_type='json');