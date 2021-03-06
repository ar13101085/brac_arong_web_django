"""brac_arong URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken import views as rest_framework_views
import aarong.views
from aarong import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^getAllProduct$', aarong.views.GetAllProduct,name="all_product"),
    url(r'^AddShop', aarong.views.AddShop,name="AddShop"),
#    url(r'^GetAllRoute', aarong.views.GetAllRoute,name="GetAllRoute"),
    url(r'^GetAllShopInRoute', aarong.views.GetAllShopInRoute,name="GetAllShopInRoute"),
    url(r'^SaleAdd', aarong.views.SaleAdd,name="GetAllShopInRoute"),
    url(r'^GetToken', aarong.views.GetToken,name="GetToken"),
    url(r'^get_auth_token/$', rest_framework_views.obtain_auth_token, name='get_auth_token'),
    url(r'^home/$', aarong.views.home, name='home'),
    url(r'^login/$', aarong.views.login, name='login'),
    url(r'^GetMarketAnalysis/$', aarong.views.GetMarketAnalysis, name='GetMarketAnalysis'),
    url(r'^GetMarketProductAnalysis/$', aarong.views.GetMarketProductAnalysis, name='GetMarketProductAnalysis'),
    url(r'^AllProductReport/$', aarong.views.AllProductReport, name='AllProductReport'),
    url(r'^GetNotification/$', aarong.views.GetNotification, name='GetNotification'),
    url(r'^GetUserSaleHistory/$', aarong.views.GetUserSaleHistory, name='GetUserSaleHistory'),
    url(r'^GetAllCategory/$', aarong.views.GetAllCategory, name='GetAllCategory'),
    url(r'^GetAllProductInCategory/$', aarong.views.GetAllProductInCategory, name='GetAllProductInCategory'),
    url(r'^GetAllArea/$', aarong.views.GetAllArea, name='GetAllArea'),
    url(r'^GetAllBranch/$', aarong.views.GetAllBranch, name='GetAllBranch'),
    url(r'^GetAllRoute/$', aarong.views.GetAllRoute, name='GetAllRoute'),
    url(r'^GetAllRouteByUser/$', aarong.views.GetAllRouteByUser, name='GetAllRouteByUser'),
    url(r'^SaleReport/$', aarong.views.SaleReport, name='SaleReport'),
    url(r'^UserRouteList/$', aarong.views.UserRouteList, name='UserRouteList'),
    url(r'^.*\.html', views.gentella_html, name='gentella'),
    url(r'^$', views.index, name='index'),
]
urlpatterns +=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
urlpatterns +=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

admin.site.site_header = "Aarong administration";
admin.site.index_title = ""
admin.site.site_title = ""