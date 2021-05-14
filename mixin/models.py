from django.db import models
from django.utils import timezone


class BaseManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(hidden=False)


class BaseModel(models.Model):
    created = models.DateTimeField(editable=False,
                                   db_index=True,
                                   verbose_name='Created at')
    modified = models.DateTimeField(db_index=True,
                                    verbose_name='Last modified')
    hidden = models.BooleanField(default=False,
                                 db_index=True,
                                 verbose_name='Hidden or deleted')

    objects = BaseManager()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.created = timezone.now()
        self.modified = timezone.now()
        super(BaseModel, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.hidden = True
        self.save()
