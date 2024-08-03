from django.db import models

class BaseModel(models.Model):
    '''base model for all models'''
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    meta = models.JSONField(default=dict)

    class Meta:
        abstract = True
