from uuid import uuid4

from django.db import models


class Genre(models.Model):

    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    categories = models.ManyToManyField('category.Category', related_name='genres')


    class Meta:
        db_table = 'genre'


    def __str__(self):
        return self.name