from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.views import APIView
from django.http import JsonResponse, HttpResponseRedirect
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from my_project.apps.url_shortener.models import Url
from my_project.apps.url_shortener.serializers.url_serializer import UrlSerializer


class UrlShortenerView(viewsets.GenericViewSet):
    serializer_class = UrlSerializer
    http_method_names = ['get', 'post']

    def get_queryset(self):
        short_url = self.request.data.GET.get('short_url')
        return Url.objects.filter(short_url=short_url)

    @action(detail=False, methods=['POST'])
    def encode(self, request):
        long_url = request.data.get('long_url', None)
        url, error_message = self.__try_encoding(long_url)
        if error_message:
            return JsonResponse({'success': False, 'message': error_message}, status=400)
        return JsonResponse({'success': True, 'url': UrlSerializer(url).data}, status=200)

    @action(detail=False, methods=['POST'])
    def decode(self, request):
        short_url = request.data.get('short_url', None)
        if not short_url:
            return JsonResponse({'success': False, 'message': 'Short url is necessary'}, status=400)
        try:
            url = Url.objects.get(short_url=short_url)
        except Url.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Url not found'}, status=404)
        return JsonResponse({'success': True, 'url': UrlSerializer(url).data}, status=200)

    def __try_encoding(self, long_url):
        url = None
        error_message = None
        if not long_url:
            error_message = 'Long url is necessary'
        if not error_message:
            try:
                url, _ = Url.objects.get_or_create(long_url=long_url)
            except ValidationError as exc:
                if exc.message == 'Enter a valid URL.':
                    error_message = 'Url is incorrect, make sure it complies to the following format. http(s)://'
        return url, error_message


class RedirectToUrl(APIView):

    def get(self, *args, **kwargs):
        short_url = kwargs.get('short_url', None)
        try:
            url = Url.objects.get(short_url=short_url)
            url.times_visited += 1
            url.save()
            return HttpResponseRedirect(redirect_to=url.long_url)
        except Url.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Url not found'}, status=404)
