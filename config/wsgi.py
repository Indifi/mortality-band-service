"""
WSGI config for analytics_furnace project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""
import os
import sys
from django.core.wsgi import get_wsgi_application


this_dir = os.path.dirname(__file__)
project_dir = os.path.dirname(this_dir)

sys.path.append(this_dir)
sys.path.append(project_dir)

application = get_wsgi_application()
