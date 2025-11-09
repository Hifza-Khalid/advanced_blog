import time
from django.utils import timezone
from django.core.cache import cache

class UserActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # Track user activity for authenticated users
        if request.user.is_authenticated:
            user_id = request.user.id
            cache_key = f'user_activity_{user_id}'
            cache.set(cache_key, timezone.now(), 300)  # Cache for 5 minutes
        
        return response