from django.apps import AppConfig


class ProfileappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ProfileApp'
    
    # Import the signals
    def ready(self):
        import ProfileApp.signals
        
