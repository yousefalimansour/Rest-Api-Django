from pickle import PUT
from sys import prefix
from typing import Self

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from django.db.models import Max
from rest_framework.response import Response
from rest_framework.decorators import api_view
from myapi.serializers import UserSerializer,ProductSerializer ,OrderSerializer , ProductInfoSerializer ,OrderCreateSerializer
from myapi.models import Product , Order , OrderItem, User
# from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
    AllowAny
)
from django_filters.rest_framework import DjangoFilterBackend
# from django.shortcuts import get_object_or_404
from myapi import serializers
from rest_framework import filters, generics, viewsets
from rest_framework.decorators import api_view, action
from rest_framework.generics import ListCreateAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView

from myapi.models import Order, OrderItem, Product
from myapi.serializers import (OrderSerializer, ProductInfoSerializer,
                               ProductSerializer)

from .filter import InStockFilter, ProductFilter,OrderFilter


class ProductListViewListCreateAPIView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    filter_backends = [
        DjangoFilterBackend,
        InStockFilter,
        filters.OrderingFilter,
        filters.SearchFilter,       
    ]
    search_fields = ['name','description']
    ordering_fields =['price','name','stock']
    pagination_class = None

    @method_decorator(cache_page(60*15, key_prefix='product_list'))
    def list(self,request,*args,**kwargs):
        return super().list(request,*args,**kwargs)
    
    def get_queryset(self):
        import time 
        time.sleep(2)
        return super().get_queryset()

    # pagination_class.page_size = 2
    # pagination_class.page_query_param = 'pagenum'
    # pagination_class.page_size_query_param = 'size'
    # pagination_class.max_page_size = 4

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == 'POST':
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_url_kwarg = 'product_id'

    def get_permission(self):
        self.permission_classes = [AllowAny]
        if self.rquest.method in ['PUT','PATCH','DELETE']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related('items__product')
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None
    filterset_class = OrderFilter
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        query = super().get_queryset()
        if not self.request.user.is_staff:
            query = query.filter(user = self.request.user)
        return query

    # @action(
    #     detail = False ,
    #     methods = ['get'],
    #     url_path = 'user-orders',
    #          )
    # def user_orders(self,request):
    #     orders = self.get_queryset().filter(user = request.user)
    #     serializer = self.get_serializer(orders, many =True)
    #     return Response(serializer.data)


    def perform_create(self,serializer):
        serializer.save(user = self.request.user)

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return OrderCreateSerializer
        return super().get_serializer_class()
        
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)


# class UserOrderListView(generics.ListAPIView):
#     queryset = Order.objects.prefetch_related('items__product')
#     serializer_class = OrderSerializer
#     permission_classes = [IsAuthenticated]


class ProductInfoAPIView(APIView):
    def get(self , request):
        products = Product.objects.all()
        serializer = ProductInfoSerializer({       
            'product': products,
            'count': len(products),
            'max_price':products.aggregate(max_price = Max('price'))['max_price'],
        })
        return Response(serializer.data)  


class UserAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = None

