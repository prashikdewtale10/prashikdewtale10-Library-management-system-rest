from django.apps import AppConfig


class LibraryConfig(AppConfig):
    name = "apps.library"

    def ready(self):
        import apps.library.signals
