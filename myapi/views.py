from pickle import PUT
from typing import Self
from django.db.models import Max
from rest_framework.response import Response
from rest_framework.decorators import api_view
from myapi.serializers import ProductSerializer ,OrderSerializer , ProductInfoSerializer
from myapi.models import Product , Order , OrderItem
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
from .filter import ProductFilter ,InStockFilter
from rest_framework import filters
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import viewsets


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
    pagination_class = LimitOffsetPagination
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
    pagination_classes = None

# class UserOrderListView(generics.ListAPIView):
#     queryset = Order.objects.prefetch_related('items__product')
#     serializer_class = OrderSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         qs = super().get_queryset()
#         return qs.filter(user=self.request.user)
    
class ProductInfoAPIView(APIView):
    def get(self , request):
        products = Product.objects.all()
        serializer = ProductInfoSerializer({       
            'product': products,
            'count': len(products),
            'max_price':products.aggregate(max_price = Max('price'))['max_price'],
        })
        return Response(serializer.data)  

