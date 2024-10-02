import os
from channels.routing import ProtocolTypeRouter
from django.core.asgi import get_asgi_application

django_asgi_app = get_asgi_application()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "That´s my shirt!.settings")
application = ProtocolTypeRouter({"http": django_asgi_app,})

ASGI_APPLICATION = 'That´s my shirt!.asgi.application'

