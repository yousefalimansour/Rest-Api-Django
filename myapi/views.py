from django.db.models import Max
from rest_framework.response import Response
from rest_framework.decorators import api_view
from myapi.serializers import ProductSerializer ,OrderSerializer , ProductInfoSerializer
from myapi.models import Product , Order , OrderItem
from django.shortcuts import get_object_or_404
from rest_framework import generics


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.exclude(stock__gt = 0)
    serializer_class = ProductSerializer

class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class OrderListView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related('items__product')
    serializer_class = OrderSerializer

@api_view(['GET'])
def product_info(request):
    products = Product.objects.all()
    serializer = ProductInfoSerializer({       
        'product': products,
        'count': len(products),
        'max_price':products.aggregate(max_price = Max('price'))['max_price'],
    })
    return Response(serializer.data)