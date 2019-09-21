"""bigmarket URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.conf.urls import url
from django.urls import path, include
from django.views.static import serve  # django访问静态文件的方法

import xadmin
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter

from apps.logistics.views import InitialRegionView
from apps.product.views import InitialCategoryView, ImportProductsView

from bigmarket.settings import MEDIA_ROOT

from apps.product.views import ProductsListViewSet, CategoryViewSet

router = DefaultRouter()
# 通过配置url
router.register(r'product/list', ProductsListViewSet, basename='Product')  # 在view重载get_queryset函数时，必须设置basename属性
router.register(r'categories', CategoryViewSet, basename='Category')

urlpatterns = [
    #    path('admin/', admin.site.urls),
    url(r'^admin/', xadmin.site.urls),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # 自动生成文档 必须要安装coreapi这个包！！！
    url(r'docs/', include_docs_urls(title='bigmarket')),

    # 配置上传文件的访问url
    url(r'^medias/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),

    # 物流管理
    url(r'^logistics/region/initial', InitialRegionView.as_view()),

    # 商品管理
    url(r'^products/categories/initial', InitialCategoryView.as_view()),
    url(r'^products/initial', ImportProductsView.as_view()),
]
