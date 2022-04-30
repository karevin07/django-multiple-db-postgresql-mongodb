from django.db import models


# Create your models here.

class Member(models.Model):
    class Meta:
        app_label = 'example_user'

    name = models.CharField(max_length=50, blank=True)
    photo = models.URLField(max_length=250)

    def __str__(self):
        return self.name
