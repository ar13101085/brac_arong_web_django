import json

import matplotlib.pyplot as plt;
import mpld3
import numpy as np
import pandas as pd;
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.http import HttpResponse
# Create your views here.
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from aarong.models import Product, Category, Shop, Route, Sale, SaleProductList


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
@permission_classes((IsAuthenticated,))
def SaleAdd(request):
    shop = Shop.objects.get(pk=request.POST['shopId']);
    user=User.objects.get(pk=request.POST['user_id'])
    total=request.POST['total'];

    sale=Sale(Shop=shop,Total=total,User=user);
    sale.save();


    saleInfo=json.loads(request.POST['sale']);
    for x in saleInfo:
        print(x)

        product=Product.objects.get(pk=x['productId'])
        saleQuantity=x['saleQuantity'];
        saleMoney=x['totalPrice'];

        saleProductList=SaleProductList(Product=product,Sale=sale,saleQuantity=saleQuantity,saleMoney=saleMoney);
        saleProductList.save();

    saveData=model_to_dict(sale);
    saveData['res']=True;
    return HttpResponse(json.dumps(saveData), content_type='json');
@csrf_exempt
def GetToken(request):
    #print("user is "+str(request.user.is_authenticated()))
    user=User.objects.filter(username=request.POST['user_name']).first();
    if user and (user.check_password(request.POST['password'])):
        token = Token.objects.get(user=user)
        if token:
            pass;
        else:
            token = Token.objects.create(user=user)
        data = model_to_dict(token);
        data['res']=True;
        return HttpResponse(json.dumps(data), content_type='json');
    else:
        data={};
        data['res']=False;
        return HttpResponse(json.dumps(data), content_type='json');

    #return HttpResponse(json.dumps(token), content_type='json');


def figure(request):

    np.random.seed(9615)

    N = 100
    df = pd.DataFrame((.1 * (np.random.random((N, 5)) - .5)).cumsum(0),
                  columns=['a', 'b', 'c', 'd', 'e'], )

    # plot line + confidence interval
    fig, ax = plt.subplots()
    ax.grid(True, alpha=0.3)

    for key, val in df.iteritems():
        l, = ax.plot(val.index, val.values, label=key)
        ax.fill_between(val.index,
                        val.values * .5, val.values * 1.5,
                        color=l.get_color(), alpha=.4)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title('Interactive legend', size=20)

    html_fig = mpld3.fig_to_html(fig,template_type='general')
    plt.close(fig)

    return render(request, "app/index.html", {'active_page' : 'dashboard.html', 'div_figure' : html_fig})