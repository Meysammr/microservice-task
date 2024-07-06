from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core.cache import cache


def cache_get_or_set(key, func, timeout=None):
    value = cache.get(key)
    if value is None:
        value = func()
        cache.set(key, value, timeout)
    return value


def cache_invalidate(key):
    cache.delete(key)


def send_notification(message):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'notifications',
        {
            'type': 'send_notification',
            'message': message,
        }
    )
