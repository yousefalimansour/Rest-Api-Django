from rest_framework.response import Response
from rest_framework.decorators import api_view
from myapi.serializers import ProductSerializer
from myapi.models import Product , Order , OrderItem
from django.shortcuts import get_object_or_404

@api_view(['GET'])
def product_list(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products , many = True)
    return Response(serializer.data)


@api_view(['GET'])
def product_detail(request , pk):
    product = get_object_or_404(Product,pk = pk)
    serializer = ProductSerializer(product)
    return Response(serializer.data)



