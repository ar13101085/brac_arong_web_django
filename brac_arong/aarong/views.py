import json

import datetime;
import matplotlib.pyplot as plt;
import matplotlib;
matplotlib.use("Agg");
import mpld3
import numpy as np
import pandas as pd;
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.models import Sum
from django.forms.models import model_to_dict
from django.http import HttpResponse
# Create your views here.
from django.shortcuts import render, redirect
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from aarong.models import Product, Category, Shop, Route, Sale, SaleProductList, OtherVendor, NiceColor, Notification, \
    Branch


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
    userName=request.GET['userName'];
    user=User.objects.filter(username=userName).first();
    branch=Branch.objects.filter(User=user).all();
    routeList=Route.objects.filter(Branch=branch).all();
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

    if request.user.is_authenticated() is not True:
        return redirect('/login');

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

def login(request):
    failed=False;

    if request.user.is_authenticated():
        return redirect('/home');

    currentDateTime=datetime.datetime.now().strftime('%Y');
    if request.method=='POST':
        user = authenticate(request,username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            auth.login(request=request,user=user);
            return redirect('/home');
        else:
            failed=True;
            template = loader.get_template('app/login.html')
            return HttpResponse(template.render({'year': currentDateTime,'failed':failed}, request));
    elif request.method=='GET':
        template = loader.get_template('app/login.html')
        return HttpResponse(template.render({'year':currentDateTime,'failed':failed}, request))



def index(request):
    if request.user.is_authenticated() is not True:
        return redirect('/login');
    # context = {}
    # template = loader.get_template('app/index.html')
    # return HttpResponse(template.render(context, request))
    return redirect('/home');


def gentella_html(request):
    if request.user.is_authenticated() is not True:
        return redirect('/login');
    context = {}
    # The template to be loaded as per gentelella.
    # All resource paths for gentelella end in .html.

    # Pick out the html file name from the url. And load that template.
    load_template = request.path.split('/')[-1]
    template = loader.get_template('app/' + load_template)
    return HttpResponse(template.render(context, request))

def home(request):
    return render(request, "app/index.html", {'active_page': 'dashboard.html'});


# def GetMarketAnalysis(request):
#     otherVendor=OtherVendor.objects.prefetch_related("other_vendor");
#     name=[];
#     taka=[];
#     for x in otherVendor:
#         list=[];
#         name.append(x.name);
#         money=x.other_vendor.all().aggregate(Sum('saleMoney'))['saleMoney__sum'];
#         if money:
#             taka.append(money);
#         else:
#             taka.append(0);
#
#     aarongSell=SaleProductList.objects.all().aggregate(Sum('saleMoney'))['saleMoney__sum'];
#     name.append("Aarong");
#     taka.append(aarongSell);
#     colorData=[];
#     color=NiceColor.objects.all();
#     for x in color:
#         colorData.append(x.code);
#     data={};
#     data['name']=name;
#     data['money']=taka;
#     data['color']=colorData;
#     return HttpResponse(json.dumps(data), content_type='json');
@csrf_exempt
def GetMarketAnalysis(request):
    categoryId=request.POST["categoryId"];
    date=request.POST["date_range"];
    dateData=date.split(" - ");
    dateStart=datetime.datetime.strptime(dateData[0],"%Y-%m-%d");
    dateEnd=datetime.datetime.strptime(dateData[1],"%Y-%m-%d");
    daterange = pd.date_range(dateStart, dateEnd)
    otherVendor = OtherVendor.objects.prefetch_related("other_vendor");
    vendor={};
    nameList=[];
    nameList.append('Aarong');
    dateList=[];
    vendor['Aarong']=[];
    listTotal=[];

    vendorList=OtherVendor.objects.all();
    for x in vendorList:
        nameList.append(x.name);
        vendor[x.name]=[];

    if int(categoryId)==-1:
        print("category id -1 "+categoryId )
        for single_date in daterange:
            dateList.append(single_date.strftime("%Y-%m-%d"));
            date=datetime.datetime.strptime(single_date.strftime("%Y-%m-%d"),"%Y-%m-%d");
            aarongSell = SaleProductList.objects.filter(CreatedTime=date).aggregate(Sum('saleMoney'))['saleMoney__sum'];
            aarongMoney=0;
            if aarongSell:
                aarongMoney = aarongSell;

            vendor['Aarong'].append(aarongMoney);
            for x in otherVendor:
                singalData={};
                money = x.other_vendor.filter(CreatedTime=date).aggregate(Sum('saleMoney'))['saleMoney__sum'];
                if money:
                    singalData['money']=money;
                else:
                    singalData['money'] = 0;

                vendor[x.name].append(singalData['money']);
    else:
        print("category id  " + categoryId)
        for single_date in daterange:
            dateList.append(single_date.strftime("%Y-%m-%d"));
            date=datetime.datetime.strptime(single_date.strftime("%Y-%m-%d"),"%Y-%m-%d");
            category = Category.objects.get(pk=int(categoryId));
            categoryAllProduct=Product.objects.filter(Category=category);
            aarongSell = SaleProductList.objects.filter(CreatedTime=date).filter(Product=categoryAllProduct).aggregate(Sum('saleMoney'))['saleMoney__sum'];
            aarongMoney=0;
            if aarongSell:
                aarongMoney = aarongSell;

            vendor['Aarong'].append(aarongMoney);
            for x in otherVendor:
                singalData={};

                money = x.other_vendor.filter(CreatedTime=date).filter(Category=category).aggregate(Sum('saleMoney'))[
                    'saleMoney__sum'];
                if money:
                    singalData['money']=money;
                else:
                    singalData['money'] = 0;

                vendor[x.name].append(singalData['money']);
    for x in nameList:
        sum=0;
        for y in vendor[x]:
            sum +=y;
        listTotal.append(sum);

    colorData = [];
    color = NiceColor.objects.all();
    for x in color:
        colorData.append(x.code);

    vendor['name']=nameList;
    vendor['date']=dateList;
    vendor['color']=colorData;
    vendor['total']=listTotal;

    return HttpResponse(json.dumps(vendor), content_type='json');

def GetMarketProductAnalysis(request):
    category=Category.objects.prefetch_related("category_name");
    name=[];
    taka=[];
    for x in category:
        list=[];
        name.append(x.CategoryName);
        money=x.category_name.all().aggregate(Sum('saleMoney'))['saleMoney__sum'];
        if money:
            taka.append(money);
        else:
            taka.append(0);

    aarongSell=SaleProductList.objects.all().aggregate(Sum('saleMoney'))['saleMoney__sum'];
    name.append("Aarong");
    taka.append(aarongSell);
    colorData=[];
    color=NiceColor.objects.all();
    for x in color:
        colorData.append(x.code);
    data={};
    data['name']=name;
    data['money']=taka;
    data['color']=colorData;
    #data={};
    return HttpResponse(json.dumps(data), content_type='json');

def AllProductReport(request):
    allProduct=Product.objects.all();
    name = [];
    taka = [];
    for a in allProduct:
        name.append(a.Category.CategoryName+" "+a.ProductName);
        sumData=SaleProductList.objects.filter(Product=a).all().aggregate(Sum('saleMoney'))['saleMoney__sum'];
        if sumData is None:
            sumData=0;
        taka.append(sumData);
    colorData = [];
    color = NiceColor.objects.all();
    for x in color:
        colorData.append(x.code);
    data = {};
    data['name'] = name;
    data['money'] = taka;
    data['color'] = colorData;
    return HttpResponse(json.dumps(data), content_type='json');
def AllProductReport(request):
    allProduct=Product.objects.all();
    name = [];
    taka = [];
    for a in allProduct:
        name.append(a.Category.CategoryName+" "+a.ProductName);
        sumData=SaleProductList.objects.filter(Product=a).all().aggregate(Sum('saleMoney'))['saleMoney__sum'];
        if sumData is None:
            sumData=0;
        taka.append(sumData);
    colorData = [];
    color = NiceColor.objects.all();
    for x in color:
        colorData.append(x.code);
    data = {};
    data['name'] = name;
    data['money'] = taka;
    data['color'] = colorData;
    return HttpResponse(json.dumps(data), content_type='json');

def GetNotification(request):
    notification=Notification.objects.all().order_by("-CreatedTime").all();
    listData=[];
    for x in notification:
        listData.append(model_to_dict(x));
    return HttpResponse(json.dumps(listData), content_type='json');
@csrf_exempt
def GetUserSaleHistory(request):
    user=User.objects.filter(username=request.POST['userName']).first();
    page=request.POST['page'];
    allSale=Sale.objects.filter(User=user);
    history=[];
    for x in allSale:
        saleProduct=SaleProductList.objects.filter(Sale=x)

        saleInfo={};
        saleInfo['shopName']=x.Shop.ShopProviderName;
        saleInfo['date']=x.OrderCreatedTime.strftime("%d-%m-%Y");
        saleInfo['saleProduct'  ]=[];
        sum=0;
        for y in saleProduct:
            product = {};
            product['name']=y.Product.ProductName;
            product['quantity']=y.saleQuantity;
            product['prize']=y.saleMoney;
            saleInfo['saleProduct'].append(product);
            sum +=y.saleMoney;
        saleInfo['total']=sum;
        history.append(saleInfo);

    return HttpResponse(json.dumps(history), content_type='json');

def GetAllProduct(request):
    categorys=Category.objects.all();
    listCategory=[];
    for x in categorys:
        category={};
        category['id']=x.CategoryId;
        category['name']=x.CategoryName;
        try:
            category['photo'] = x.CategoryPhoto.url;
        except:
            category['photo']='';

            listCategory.append(category);

    return HttpResponse(json.dumps(listCategory), content_type='json');