from django.contrib import admin

from my_project.apps.url_shortener.models import Url


@admin.register(Url)
class UrlAdmin(admin.ModelAdmin):
    list_display = ('long_url', 'short_url', 'times_visited')
    readonly_fields = ('short_url', 'times_visited')
