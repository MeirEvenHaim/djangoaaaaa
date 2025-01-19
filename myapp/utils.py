from django.core.cache import cache
import json
import logging

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
        # Deserialize JSON data from cache to get the actual value
        deserialized_data = json.loads(cached_data)
        logger.info(f"Cache hit for key: {key}, value: {deserialized_data}")
        return deserialized_data

    logger.info(f"Cache miss for key: {key}. Fetching and caching data.")
    # Fetch data using the callback function
    data = callback()
    logger.info(f"Fetched data for key: {key}, value: {data}")
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




    

