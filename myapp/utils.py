from django.core.cache import cache
from django.shortcuts import render
import json
import logging
from paypalrestsdk import Webhook
from myapp.views.paymentView import get_paypal_client


logger = logging.getLogger(__name__)

def get_or_set_cache(key, callback, timeout=300):
    """
    Retrieve data from cache or execute callback to fetch and cache the data.
    The data is serialized as JSON before being stored in cache and deserialized
    when retrieved.

    :param key: Cache key
    :param callback: Function to call to fetch data if not in cache
    :param timeout: Time in seconds for cache to expire
    :return: Cached or newly fetched data
    """
    # Try to get the cached data
    cached_data = cache.get(key)
    if cached_data is not None:
        logger.info(f"Cache hit for key: {key}")
        # Deserialize JSON data from cache
        return json.loads(cached_data)

    logger.info(f"Cache miss for key: {key}. Fetching and caching data.")
    # Fetch data using the callback function
    data = callback()
    # Serialize data to JSON before caching
    serialized_data = json.dumps(data)
    # Store serialized data in cache
    cache.set(key, serialized_data, timeout=timeout)
    return data

def delete_cache(key):
    """
    Deletes a cache entry by its key.
    """
    logger.info(f"Deleting cache for key: {key}")
    cache.delete(key)

def get_client_ip(request):
    """Utility function to get client IP address."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip



def log_with_context(logger, request, message, level='info'):
    """Utility function to log with contextual info."""
    user = getattr(request, 'user', None)
    if user.is_authenticated:
        user = user.username
    else:
        user = 'Anonymous'

    extra = {
        'client_ip': get_client_ip(request),
        'user': user,
        'method': request.method,
        'path': request.path,
    }

    log_method = getattr(logger, level, 'info')
    log_method(message, extra=extra)


    


def create_webhook():
    client = get_paypal_client()
    webhook = Webhook({
        "url": "https://your-domain.com/webhook/",
        "event_types": [
            {"name": "PAYMENT.CAPTURE.COMPLETED"},
            {"name": "CHECKOUT.ORDER.APPROVED"}
        ]
    })

    if webhook.create():
        print("Webhook created successfully:", webhook.id)
        return webhook.id
    else:
        print("Failed to create webhook:", webhook.error)

