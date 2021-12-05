from django.db import models
from django.core.validators import URLValidator

from my_project.apps.url_shortener.encode_strategies.shake_256_hexdigest_strategy import Hex256HexdigestStrategy


class Url(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    long_url = models.URLField()
    short_url = models.CharField(max_length=8, unique=True, blank=True)
    times_visited = models.PositiveIntegerField(default=0)

    __original_long_url = None

    def __str__(self):
        return self.long_url

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_long_url = self.long_url

    def save(self, *args, **kwargs):
        #   Prevents regenerating short url if the long url was not changed
        if not self.pk or (self.long_url != self.__original_long_url):
            self.clean()
        super().save(*args, **kwargs)

    def clean(self):
        validator = URLValidator()
        validator(self.long_url)
        self.__generate_short_url()

    def __generate_short_url(self):
        encoder_strategy = Hex256HexdigestStrategy()
        self.short_url = encoder_strategy.encode(self.long_url)
