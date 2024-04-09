# your_app/context_processors.py
from .models import Notification

def notifications(request):
    if request.user.is_authenticated:
        return {
            'global_notifications': Notification.objects.filter(to_user=request.user, is_read=False)
        }
    return {}
