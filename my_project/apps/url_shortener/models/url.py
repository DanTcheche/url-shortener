from django.db import models


class Url(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    long_url = models.URLField()
    short_url = models.CharField(max_length=8, unique=True, blank=True)
    times_visited = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.long_url
