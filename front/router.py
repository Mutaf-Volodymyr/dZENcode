from django.urls import re_path
from front.consumers import CommentConsumer



ws_urlpatterns = [
    re_path(r"ws/comments/$", CommentConsumer.as_asgi()),
]