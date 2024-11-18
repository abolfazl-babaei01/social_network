from datetime import timedelta
from django.utils import timezone
from .models import Story

class ExpiredStoriesMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        expiration_time = timezone.now() - timedelta(minutes=60)
        Story.objects.filter(created_at__lt=expiration_time, is_delete=False).update(is_delete=True)

        response = self.get_response(request)
        return response
