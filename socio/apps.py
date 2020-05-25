from django.apps import AppConfig


class SocioConfig(AppConfig):
    name = 'socio'

    def ready(self):
    	import socio.signals
