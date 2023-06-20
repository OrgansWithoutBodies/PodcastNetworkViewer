from django.apps import AppConfig


class NetConfig(AppConfig):
    name = 'Net'
    app_label='Net'
    def ready(self):
    	import Net.signals
