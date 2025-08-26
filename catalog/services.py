from django.core.cache import cache
from catalog.models import Product

def get_products_by_category(category_id):
    cache_key = f'products_category_{category_id}'
    products = cache.get(cache_key)
    
    if products is None:
        products = list(Product.objects.filter(
            category_id=category_id, 
            publish_status='published'
        ).order_by('-created_at'))
        cache.set(cache_key, products, 60 * 15)
    
    return products