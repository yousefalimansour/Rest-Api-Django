from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Order, Product
from django.core.cache import cache

@receiver([post_delete,post_save],sender= Product)
def invalid_product_cache(sender, instance,**kwargs):
    """
    Invalidate product list caches when a product is created, updated, or deleted
    """
    print("Cache Cleaned for product!")

    cache.delete_pattern('*product_list*')

@receiver([post_delete,post_save],sender= Order)
def invalid_product_cache(sender, instance,**kwargs):
    """
    Invalidate order list caches when a product is created, updated, or deleted
    """
    print("Cache Cleaned for Order!")

    cache.delete_pattern('*order_list*')