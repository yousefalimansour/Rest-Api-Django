from dataclasses import fields
import django_filters
from .models import Order, Product
from rest_framework import filters



class InStockFilter(filters.BaseFilterBackend):
    def filter_queryset(self ,request,queryset,view):
        return queryset.filter(stock__gt = 0)

class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = {
            'name':['exact','icontains'],
            'price':['exact', 'lt', 'gt', 'range'],
        }

class OrderFilter(django_filters.FilterSet):
    created_at = django_filters.DateFilter(field_name='created_at__date')
    class Meta:
        model = Order
        fields = {
            'status':['exact'],
            'created_at':['exact', 'lt', 'gt'],
        }