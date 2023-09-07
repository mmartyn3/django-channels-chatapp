"""
ASGI config for mysite project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from chat_app.routing import websocket_urlpatterns


# Set the default Django settings module for the ASGI application.
# This ensures that the AppRegistry is populated before importing code that
# may require ORM models.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

# Initialize the Django ASGI application early to populate the AppRegistry.
django_asgi_app = get_asgi_application()

def create_protocol_type_router() -> ProtocolTypeRouter:
    """
    Create a ProtocolTypeRouter for the Django ASGI application.

    Returns:
        ProtocolTypeRouter: The protocol router configured with HTTP and WebSocket protocols.
    """
    return ProtocolTypeRouter(
        {
            "http": django_asgi_app,  # Route HTTP requests to the Django ASGI application.
            # Route WebSocket requests through AllowedHostsOriginValidator and AuthMiddlewareStack.
            "websocket": AllowedHostsOriginValidator(
                AuthMiddlewareStack(
                    URLRouter(websocket_urlpatterns)  # Route WebSocket requests to the defined URL patterns.
                )
            ),
        }
    )

# Create the ASGI application.
application: ProtocolTypeRouter = create_protocol_type_router()
