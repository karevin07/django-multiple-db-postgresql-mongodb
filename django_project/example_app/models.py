from django.db import models
from django.utils.timezone import now
from django_mongodb_backend.fields import ObjectIdAutoField


# Create your models here.

class Post(models.Model):
    class Meta:
        app_label = 'example_app'

    id = ObjectIdAutoField(primary_key=True)
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    content = models.TextField()
    datetime = models.DateField(default=now)

    def __str__(self):
        return self.title
