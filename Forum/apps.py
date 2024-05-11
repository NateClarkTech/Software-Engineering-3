from django.apps import AppConfig

#@W_Farmer
# Mostly auto generated except for the signals
class ForumConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    app_name = 'Forum'
    name = 'Forum'
    
    # Import the signals
    def ready(self):
        import Forum.signals
