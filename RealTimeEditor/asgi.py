# # """
# # ASGI config for RealTimeEditor project.

# # It exposes the ASGI callable as a module-level variable named ``application``.

# # For more information on this file, see
# # https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
# # """

# # import os

# # from django.core.asgi import get_asgi_application

# # os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RealTimeEditor.settings')

# # application = get_asgi_application()


# # liveeditor/asgi.py

# import os
# from channels.routing import ProtocolTypeRouter, URLRouter
# from django.core.asgi import get_asgi_application
# from channels.auth import AuthMiddlewareStack
# import App.routing

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RealTimeEditor.settings')

# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     "websocket": AuthMiddlewareStack(
#         URLRouter(
#             App.routing.websocket_urlpattern
#         )
#     ),
# })


import os

from django.core.asgi import get_asgi_application # type: ignore
from channels.routing import ProtocolTypeRouter, URLRouter # type: ignore
import App.routing
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RealTimeEditor.settings')

application = ProtocolTypeRouter({
    'http' : get_asgi_application(),
    'websocket': URLRouter(
        App.routing.websocket_urlpatterns
    ),
})

