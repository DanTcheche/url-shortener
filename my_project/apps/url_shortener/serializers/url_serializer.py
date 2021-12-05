from rest_framework import serializers

from my_project.apps.url_shortener.models import Url


class UrlSerializer(serializers.ModelSerializer):

    class Meta:
        model = Url
        fields = ('long_url', 'short_url')
        read_only_fields = ['short_url']
