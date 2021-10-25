# import os

# from django.core.asgi import get_asgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qfit.settings')

# application = get_asgi_application()



import os
import django
from channels.routing import get_default_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qfit.settings')
django.setup()
application = get_default_application()



# import os
# from channels.asgi import get_channel_layer

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "qfit.settings")

# channel_layer = get_channel_layer()


