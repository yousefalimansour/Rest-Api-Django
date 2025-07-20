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

class ProductListViewListCreateAPIView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == 'POST':
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class OrderListView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related('items__product')
    serializer_class = OrderSerializer

class UserOrderListView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related('items__product')
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)
    

class ProductInfoAPIView(APIView):
    def get(self , request):
        products = Product.objects.all()
        serializer = ProductInfoSerializer({       
            'product': products,
            'count': len(products),
            'max_price':products.aggregate(max_price = Max('price'))['max_price'],
        })
        return Response(serializer.data)  

