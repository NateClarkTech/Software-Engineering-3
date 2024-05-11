# your_app/context_processors.py
from .models import Notification

# This context processor will add the global notifications to the context of every request
def notifications(request):
    if request.user.is_authenticated:
        return {
            # sort them by is_read and created_at
            'global_notifications': Notification.objects.filter(to_user=request.user, is_read=False).order_by('-date')
        }
    return {}
