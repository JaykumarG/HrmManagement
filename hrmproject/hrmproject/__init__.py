from .celery import app as celery_app 

#This ensures Celery starts automatically when Django starts.

__all__ = ('celery_app',)
