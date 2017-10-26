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
    Branch, Area, AppUser


def GetAllShopInRoute(request):
    route = Route.objects.get(pk=request.GET.get('id'))
    allShop = Shop.objects.filter(Route=route).all();

    shops = [];
    for x in allShop:
        shop = model_to_dict(x);
        if x.ShopPhoto:
            shop['ShopPhoto'] = x.ShopPhoto.url;
        else:
            shop['ShopPhoto'] = '';
        shops.append(shop);
    return HttpResponse(json.dumps(shops), content_type='json');


# def GetAllRoute(request):
#     userName = request.GET['userName'];
#     user = User.objects.filter(username=userName).first();
#     branch = Branch.objects.filter(User=user).all();
#     routeList = Route.objects.filter(Branch=branch).all();
#     routes = [];
#     for x in routeList:
#         routes.append(model_to_dict(x));
#     return HttpResponse(json.dumps(routes), content_type='json');


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
    shopId = request.GET.get('shopId');  # next time use for suggetion product
    print("shop id is " + str(shopId));
    allCategory = Category.objects.all();
    all = [];
    for x in allCategory:
        data = {};
        data['CategoryId'] = x.CategoryId;
        data['CategoryName'] = x.CategoryName;
        if x.CategoryPhoto:
            data['CategoryPhoto'] = x.CategoryPhoto.url;
        else:
            data['CategoryPhoto'] = '';
        data['ProductList'] = [];
        categoryProduct = Product.objects.filter(Category=x).all();
        for y in categoryProduct:
            product = {};
            product['ProductId'] = y.ProductId;
            product['ProductName'] = y.ProductName;
            product['ProductUnitPrice'] = y.ProductUnitPrice;
            if y.ProductPhoto:
                product['ProductPhoto'] = y.ProductPhoto.url;
            else:
                product['ProductPhoto'] = '';
            data['ProductList'].append(product);
        all.append(data);

    return HttpResponse(json.dumps(all), content_type='json');


@csrf_exempt
def AddShop(request):
    route = Route.objects.get(pk=request.POST['RouteId']);
    res = {};
    if route:
        shop = Shop(ShopLat=request.POST['ShopLat'], ShopLng=request.POST['ShopLng'],
                    ShopProviderName=request.POST['ShopProviderName'], ShopGpsAddress=request.POST['ShopGpsAddress'],
                    ShopDetailsAddress=request.POST['ShopDetailsAddress'],
                    Route=route, ShopPhoto=request.FILES['ShopPhoto']);
        shop.save();
        newShop = model_to_dict(shop);
        newShop['ShopPhoto'] = newShop['ShopPhoto'].url;
        res = {'res': True, 'msg': 'successfully add shop', 'shop': newShop};
        return HttpResponse(json.dumps(res), content_type='json');
    else:
        res = {'res': False, 'msg': 'no route id found', 'shop': {}};
        return HttpResponse(json.dumps(res), content_type='json');


@csrf_exempt
@permission_classes((IsAuthenticated,))
def SaleAdd(request):
    shop = Shop.objects.get(pk=request.POST['shopId']);
    user = User.objects.filter(username=request.POST['user_id']).first();
    total = request.POST['total'];

    sale = Sale(Shop=shop, Total=total, User=user);
    sale.save();

    saleInfo = json.loads(request.POST['sale']);
    for x in saleInfo:
        print(x)

        product = Product.objects.get(pk=x['productId'])
        saleQuantity = x['saleQuantity'];
        saleMoney = x['totalPrice'];

        saleProductList = SaleProductList(Product=product, Sale=sale, saleQuantity=saleQuantity, saleMoney=saleMoney);
        saleProductList.save();

    saveData = model_to_dict(sale);
    saveData['res'] = True;
    return HttpResponse(json.dumps(saveData), content_type='json');


@csrf_exempt
def GetToken(request):
    # print("user is "+str(request.user.is_authenticated()))
    user = User.objects.filter(username=request.POST['user_name']).first();
    if user and (user.check_password(request.POST['password'])):
        token = Token.objects.get(user=user)
        if token:
            pass;
        else:
            token = Token.objects.create(user=user)

        appUser=AppUser.objects.filter(user=user).first();
        data = model_to_dict(token);
        data['res'] = True;
        data['pic']=appUser.picture.url;
        return HttpResponse(json.dumps(data), content_type='json');
    else:
        data = {};
        data['res'] = False;
        return HttpResponse(json.dumps(data), content_type='json');

        # return HttpResponse(json.dumps(token), content_type='json');


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

    html_fig = mpld3.fig_to_html(fig, template_type='general')
    plt.close(fig)

    return render(request, "app/index.html", {'active_page': 'dashboard.html', 'div_figure': html_fig})


def login(request):
    failed = False;

    if request.user.is_authenticated():
        return redirect('/home');

    currentDateTime = datetime.datetime.now().strftime('%Y');
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            auth.login(request=request, user=user);
            return redirect('/home');
        else:
            failed = True;
            template = loader.get_template('app/login.html')
            return HttpResponse(template.render({'year': currentDateTime, 'failed': failed}, request));
    elif request.method == 'GET':
        template = loader.get_template('app/login.html')
        return HttpResponse(template.render({'year': currentDateTime, 'failed': failed}, request))


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
def GetMarketProductAnalysis(request):
    category = Category.objects.prefetch_related("category_name");
    name = [];
    taka = [];
    for x in category:
        list = [];
        name.append(x.CategoryName);
        money = x.category_name.all().aggregate(Sum('saleMoney'))['saleMoney__sum'];
        if money:
            taka.append(money);
        else:
            taka.append(0);

    aarongSell = SaleProductList.objects.all().aggregate(Sum('saleMoney'))['saleMoney__sum'];
    name.append("Aarong");
    taka.append(aarongSell);
    colorData = [];
    color = NiceColor.objects.all();
    for x in color:
        colorData.append(x.code);
    data = {};
    data['name'] = name;
    data['money'] = taka;
    data['color'] = colorData;
    # data={};
    return HttpResponse(json.dumps(data), content_type='json');


def AllProductReport(request):
    allProduct = Product.objects.all();
    name = [];
    taka = [];
    for a in allProduct:
        name.append(a.Category.CategoryName + " " + a.ProductName);
        sumData = SaleProductList.objects.filter(Product=a).all().aggregate(Sum('saleMoney'))['saleMoney__sum'];
        if sumData is None:
            sumData = 0;
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
    allProduct = Product.objects.all();
    name = [];
    taka = [];
    for a in allProduct:
        name.append(a.Category.CategoryName + " " + a.ProductName);
        sumData = SaleProductList.objects.filter(Product=a).all().aggregate(Sum('saleMoney'))['saleMoney__sum'];
        if sumData is None:
            sumData = 0;
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
    notification = Notification.objects.all().order_by("-CreatedTime").all();
    listData = [];
    for x in notification:
        listData.append(model_to_dict(x));
    return HttpResponse(json.dumps(listData), content_type='json');


@csrf_exempt
def GetUserSaleHistory(request):
    user = User.objects.filter(username=request.POST['userName']).first();
    page = request.POST['page'];
    allSale = Sale.objects.filter(User=user);
    history = [];
    for x in allSale:
        saleProduct = SaleProductList.objects.filter(Sale=x)

        saleInfo = {};
        saleInfo['shopName'] = x.Shop.ShopProviderName;
        saleInfo['date'] = x.OrderCreatedTime.strftime("%d-%m-%Y");
        saleInfo['saleProduct'] = [];
        sum = 0;
        for y in saleProduct:
            product = {};
            product['name'] = y.Product.ProductName;
            product['quantity'] = y.saleQuantity;
            product['prize'] = y.saleMoney;
            saleInfo['saleProduct'].append(product);
            sum += y.saleMoney;
        saleInfo['total'] = sum;
        history.append(saleInfo);

    return HttpResponse(json.dumps(history), content_type='json');


def GetAllCategory(request):
    categorys = Category.objects.all();
    listCategory = [];
    for x in categorys:
        category = {};
        category['id'] = x.CategoryId;
        category['name'] = x.CategoryName;
        try:
            category['photo'] = x.CategoryPhoto.url;
        except:
            category['photo'] = '';

        listCategory.append(category);

    return HttpResponse(json.dumps(listCategory), content_type='json');


def GetAllProductInCategory(request):
    products = Product.objects.filter(Category=request.GET['categoryId']).all();
    listproduct = [];
    for x in products:
        product = {};
        product['id'] = x.ProductId;
        product['name'] = x.ProductName;
        try:
            product['photo'] = x.CategoryPhoto.url;
        except:
            product['photo'] = '';

        listproduct.append(product);

    return HttpResponse(json.dumps(listproduct), content_type='json');


def GetAllArea(request):
    area = Area.objects.all();
    areaList = [];
    for x in area:
        areaList.append(model_to_dict(x));
    return HttpResponse(json.dumps(areaList), content_type='json');


def GetAllBranch(request):
    branch = Branch.objects.filter(Area=request.GET['areaId']).all();
    branchList = [];
    for x in branch:
        branchList.append(model_to_dict(x));
    return HttpResponse(json.dumps(branchList), content_type='json');


def GetAllRoute(request):
    route = Route.objects.filter(Branch=request.GET['branchId']).all();
    routeList = [];
    for x in route:
        routeList.append(model_to_dict(x));
    return HttpResponse(json.dumps(routeList), content_type='json');
def GetAllRouteByUser(request):
    user=User.objects.filter(username=request.GET['userId']).first();
    branch=Branch.objects.filter(User=user).first();
    route = Route.objects.filter(Branch=branch).all();
    routeList = [];
    for x in route:
        routeList.append(model_to_dict(x));
    return HttpResponse(json.dumps(routeList), content_type='json');


@csrf_exempt
def SaleReport(request):
    areaId = int(request.POST['areaId']);
    branchId = int(request.POST['branchId']);
    routeId = int(request.POST['routeId']);
    categoryId = int(request.POST['categoryId']);
    productId = int(request.POST['productId']);
    # Working with date
    date = request.POST["date_range"];
    dateData = date.split(" - ");
    dateStart = datetime.datetime.strptime(dateData[0], "%Y-%m-%d");
    dateEnd = datetime.datetime.strptime(dateData[1], "%Y-%m-%d");
    daterange = pd.date_range(dateStart, dateEnd)

    listAarongProduct=[];
    listAarongProductSaleByDate={};
    listAarongProductQuantityByDate={};
    allAarongProduct=Product.objects.all();
    for x in allAarongProduct:
        listAarongProduct.append(x.Category.CategoryName+" "+x.ProductName);
        listAarongProductSaleByDate[x.Category.CategoryName+" "+x.ProductName]=[];
        listAarongProductQuantityByDate[x.Category.CategoryName+" "+x.ProductName]=[];




    allProduct = Product.objects.none();

    product = Product.objects.filter(ProductId=productId).all();
    if len(product)==0:
        category = Category.objects.filter(CategoryId=categoryId).first();
        if category is None:
            print("category not found")
            products = Product.objects.all();
            allProduct = products;
        else:
            print("category else")
            products = Product.objects.filter(Category=category).all();
            allProduct = products;
    else:
        print("product else")
        allProduct = product;

    print(allProduct)
    allSale = [];
    dateList = [];
    if routeId == -1:
        if branchId == -1:
            if areaId == -1:
                for single_date in daterange:
                    dateList.append(single_date.strftime("%Y-%m-%d"));
                    date = datetime.datetime.strptime(single_date.strftime("%Y-%m-%d"), "%Y-%m-%d");
                    sale = SaleProductList.objects.filter(CreatedTime=date).filter(Product__in=allProduct).aggregate(
                        Sum('saleMoney'))['saleMoney__sum'];
                    if sale is None:
                        sale = 0;
                    allSale.append(sale)
                    for p in allAarongProduct:
                        sale = SaleProductList.objects.filter(CreatedTime=date).filter(Product=p).aggregate(
                            Sum('saleMoney'),Sum('saleQuantity'));
                        if sale['saleMoney__sum'] is None:
                            sale['saleMoney__sum'] = 0;

                        if sale['saleQuantity__sum'] is None:
                            sale['saleQuantity__sum'] = 0;
                        listAarongProductSaleByDate[p.Category.CategoryName+" "+p.ProductName].append(sale['saleMoney__sum']);
                        listAarongProductQuantityByDate[p.Category.CategoryName+" "+p.ProductName].append(sale['saleQuantity__sum']);

            else:
                print("Area id found")
                area = Area.objects.filter(id=areaId).first();
                allBranch = Branch.objects.filter(Area=area).all();
                allRoute = Route.objects.filter(Branch__in=allBranch).all();
                allShop = Shop.objects.filter(Route__in=allRoute).all();
                allShopSale = Sale.objects.filter(Shop__in=allShop).all();
                for single_date in daterange:
                    dateList.append(single_date.strftime("%Y-%m-%d"));
                    date = datetime.datetime.strptime(single_date.strftime("%Y-%m-%d"), "%Y-%m-%d");
                    sale = SaleProductList.objects.filter(CreatedTime=date).filter(Sale__in=allShopSale).filter(
                        Product__in=allProduct).aggregate(Sum('saleMoney'))['saleMoney__sum'];
                    if sale is None:
                        sale = 0;
                    allSale.append(sale)
                    for p in allAarongProduct:
                        sale = SaleProductList.objects.filter(CreatedTime=date).filter(Sale__in=allShopSale).filter(
                            Product=p).aggregate(Sum('saleMoney'))['saleMoney__sum'];
                        if sale is None:
                            sale = 0;
                        listAarongProductSaleByDate[p.Category.CategoryName+" "+p.ProductName].append(sale);
        else:
            print("branch id found")
            allBranch = Branch.objects.get(pk=branchId);
            print(allBranch)
            allRoute = Route.objects.filter(Branch=allBranch).all();
            print(allRoute)
            allShop = Shop.objects.filter(Route__in=allRoute).all();
            print(allShop)
            allShopSale = Sale.objects.filter(Shop__in=allShop).all();
            for single_date in daterange:
                dateList.append(single_date.strftime("%Y-%m-%d"));
                date = datetime.datetime.strptime(single_date.strftime("%Y-%m-%d"), "%Y-%m-%d");
                sale = SaleProductList.objects.filter(CreatedTime=date).filter(Sale__in=allShopSale).filter(
                    Product__in=allProduct).aggregate(Sum('saleMoney'))['saleMoney__sum'];
                if sale is None:
                    sale = 0;
                allSale.append(sale)
                for p in allAarongProduct:
                    sale = SaleProductList.objects.filter(CreatedTime=date).filter(Sale__in=allShopSale).filter(
                        Product=p).aggregate(Sum('saleMoney'))['saleMoney__sum'];
                    if sale is None:
                        sale = 0;
                    listAarongProductSaleByDate[p.Category.CategoryName + " " + p.ProductName].append(sale)
    else:
        print("route id found")
        allRoute = Route.objects.filter(RouteId=routeId).first();
        allShop = Shop.objects.filter(Route=allRoute).all();
        allShopSale = Sale.objects.filter(Shop__in=allShop).all();
        for single_date in daterange:
            dateList.append(single_date.strftime("%Y-%m-%d"));
            date = datetime.datetime.strptime(single_date.strftime("%Y-%m-%d"), "%Y-%m-%d");
            sale = SaleProductList.objects.filter(CreatedTime=date).filter(Sale__in=allShopSale).filter(
                Product__in=allProduct).aggregate(Sum('saleMoney'))['saleMoney__sum'];
            if sale is None:
                sale = 0;
            allSale.append(sale)
            for p in allAarongProduct:
                sale = SaleProductList.objects.filter(CreatedTime=date).filter(Sale__in=allShopSale).filter(
                    Product=allProduct).aggregate(Sum('saleMoney'))['saleMoney__sum'];
                if sale is None:
                    sale = 0;
                listAarongProductSaleByDate[p.Category.CategoryName + " " + p.ProductName].append(sale)

    productVsTaka=[];
    for p in allAarongProduct:
        sum=0;
        for x in listAarongProductSaleByDate[p.Category.CategoryName + " " + p.ProductName]:
            sum +=x;
        productVsTaka.append(sum);

    colorData = [];
    color = NiceColor.objects.all();
    for x in color:
        colorData.append(x.code);

    data = {};
    data['totalSale'] = allSale;
    data['dateList'] = dateList;
    data['AarongAllProduct']=listAarongProduct;
    data['listAarongProductSaleByDate']=listAarongProductSaleByDate;
    data['listAarongProductQuantityByDate']=listAarongProductQuantityByDate;
    data['productVsTaka']=productVsTaka;
    data['color']=colorData;

    return HttpResponse(json.dumps(data), content_type='json');


# def GetAllShop(allRoute,categoryId,productId):
#     if productId==-1:
#         if categoryId==-1:
#             pass
#         else:
#             pass
#     else:
#         pass
@csrf_exempt
def GetMarketAnalysis(request):
    categoryId = request.POST["categoryId"];
    date = request.POST["date_range"];
    dateData = date.split(" - ");
    dateStart = datetime.datetime.strptime(dateData[0], "%Y-%m-%d");
    dateEnd = datetime.datetime.strptime(dateData[1], "%Y-%m-%d");
    daterange = pd.date_range(dateStart, dateEnd)
    otherVendor = OtherVendor.objects.prefetch_related("other_vendor");
    vendor = {};
    nameList = [];
    nameList.append('Aarong');
    dateList = [];
    vendor['Aarong'] = [];
    listTotal = [];

    vendorList = OtherVendor.objects.all();
    for x in vendorList:
        nameList.append(x.name);
        vendor[x.name] = [];

    if int(categoryId) == -1:
        print("category id -1 " + categoryId)
        for single_date in daterange:
            dateList.append(single_date.strftime("%Y-%m-%d"));
            date = datetime.datetime.strptime(single_date.strftime("%Y-%m-%d"), "%Y-%m-%d");
            aarongSell = SaleProductList.objects.filter(CreatedTime=date).aggregate(Sum('saleMoney'))['saleMoney__sum'];
            aarongMoney = 0;
            if aarongSell:
                aarongMoney = aarongSell;

            vendor['Aarong'].append(aarongMoney);
            for x in otherVendor:
                singalData = {};
                money = x.other_vendor.filter(CreatedTime=date).aggregate(Sum('saleMoney'))['saleMoney__sum'];
                if money:
                    singalData['money'] = money;
                else:
                    singalData['money'] = 0;

                vendor[x.name].append(singalData['money']);
    else:
        print("category id  " + categoryId)
        for single_date in daterange:
            dateList.append(single_date.strftime("%Y-%m-%d"));
            date = datetime.datetime.strptime(single_date.strftime("%Y-%m-%d"), "%Y-%m-%d");
            category = Category.objects.get(pk=int(categoryId));
            categoryAllProduct = Product.objects.filter(Category=category);
            aarongSell = SaleProductList.objects.filter(CreatedTime=date).filter(Product__in=categoryAllProduct).aggregate(
                Sum('saleMoney'))['saleMoney__sum'];
            aarongMoney = 0;
            if aarongSell:
                aarongMoney = aarongSell;

            vendor['Aarong'].append(aarongMoney);
            for x in otherVendor:
                singalData = {};

                money = x.other_vendor.filter(CreatedTime=date).filter(Category=category).aggregate(Sum('saleMoney'))[
                    'saleMoney__sum'];
                if money:
                    singalData['money'] = money;
                else:
                    singalData['money'] = 0;

                vendor[x.name].append(singalData['money']);
    for x in nameList:
        sum = 0;
        for y in vendor[x]:
            sum += y;
        listTotal.append(sum);

    colorData = [];
    color = NiceColor.objects.all();
    for x in color:
        colorData.append(x.code);

    vendor['name'] = nameList;
    vendor['date'] = dateList;
    vendor['color'] = colorData;
    vendor['total'] = listTotal;

    return HttpResponse(json.dumps(vendor), content_type='json');
