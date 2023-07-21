from django.apps import AppConfig
from wagtail.images.apps import WagtailImagesAppConfig


class CustomImagesAppConfig(WagtailImagesAppConfig):
    default_attrs = {"decoding": "async", "loading": "lazy"}

class UserInterfaceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user_interface'
