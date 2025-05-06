from time import sleep

from django.core.cache import caches  # Используем конкретный кеш
from asgiref.sync import async_to_sync
from celery import shared_task
from channels.layers import get_channel_layer
import requests

from base.utils.file_manager import check_image

redis_cache = caches["default"]


def fetch_comments():
    comments = redis_cache.get("comments_data")

    if not comments:
        try:
            response = requests.get("http://web:8000/api/v1/comments/comments/?ordering=-rating")
            response.raise_for_status()
            comments = response.json()

            redis_cache.set("comments_data", comments, timeout=10)
        except requests.RequestException as e:
            print(f"Request error: {e}")
            comments = []
    return comments


@shared_task
def send_comment_updates():
    if redis_cache.get("update_flag") is None:
        redis_cache.set("update_flag", True, timeout=5)

        channel_layer = get_channel_layer()
        comments = fetch_comments()

        async_to_sync(channel_layer.group_send)(
            "comments",
            {
                "type": "send_update",
                "comments": comments
            }
        )


@shared_task
def resize_image_task(file_path, file_extension):
    check_image(file_path=file_path, file_extension=file_extension)

