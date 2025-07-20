from rest_framework import serializers
from .models import Product , Order, OrderItem

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'description',
            'name',
            'price',
            'stock',            
        )

    def validate_price(self,value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than 0")
        return value


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source = 'product.name')
    product_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        source = 'product.price'
    )

    class Meta:
        model = OrderItem
        fields = (
            'product_name',
            'product_price',
            'quantity',
            'Item_Subtotal',
        )

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many = True , read_only = True)
    total_price = serializers.SerializerMethodField(method_name = 'total')
    def total(self , obj):
        order_items = obj.items.all()
        return sum( item.Item_Subtotal for item in order_items)

    class Meta:
        model = Order
        fields = (
            'id',
            'created_at',
            'user',
            'status',
            'items',
            'total_price',
        )

class ProductInfoSerializer(serializers.Serializer):
    product = ProductSerializer(many = True)
    count = serializers.IntegerField()
    max_price = serializers.FloatField() 