from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Product
from django.core.cache import cache

@receiver([post_delete,post_save],sender= Product)
def invalid_product_cache(sender, instance,**kwargs):
    """
    Invalidate product list caches when a product is created, updated, or deleted
    """
    print("Cache Cleaned!")

    cache.delete_pattern('*product_list*')