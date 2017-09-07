from django.http import HttpResponse
from django.shortcuts import render
from django.core import serializers
# Create your views here.
from aarong.models import Product, Category


def GetAllProduct(request):
    productList=Product.objects.all().select_related();
    # productData=[];
    # for data in productList:
    #     #data.Category=data.Category.CategoryName;
    #     x=data;
    #     x.category=Category.objects.get(pk=data.Category_id);
    #     productData.append(x)
    allProduct=serializers.serialize('json',productList);
    return HttpResponse(allProduct, content_type='json');