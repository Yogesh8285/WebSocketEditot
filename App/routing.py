from django.urls import path
from App import consumers

websocket_urlpatterns = [
path('ws/editor/<doc_id>', consumers.EditorConsumer.as_asgi()),
]