from django.db.models.manager import Manager

class BaseManager(Manager):
    '''base manager for all models'''
    def get_queryset(self):
        '''excludes deleted objects from returned queryset'''
        return super().get_queryset().exclude(status="DELETED")
