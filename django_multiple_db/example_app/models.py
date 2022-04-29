from djongo import models as djongo_models
from django.utils.timezone import now


# Create your models here.

class Post(djongo_models.Model):
    class Meta:
        app_label = 'example_app'

    _id = djongo_models.ObjectIdField()
    title = djongo_models.CharField(max_length=50)
    author = djongo_models.CharField(max_length=50)
    content = djongo_models.TextField()
    datetime = djongo_models.DateField(default=now)

    def __str__(self):
        return self.title
