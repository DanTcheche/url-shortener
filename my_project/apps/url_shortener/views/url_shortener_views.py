from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.views import APIView
from django.http import JsonResponse, HttpResponseRedirect

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
        if not long_url:
            return JsonResponse({'success': False, 'message': 'Long url is necessary'}, status=400)
        url, _ = Url.objects.get_or_create(long_url=long_url)
        return JsonResponse({'success': True, 'url': UrlSerializer(url).data}, status=400)

    @action(detail=False, methods=['POST'])
    def decode(self, request):
        short_url = request.data.get('short_url', None)
        if not short_url:
            return JsonResponse({'success': False, 'message': 'Short url is necessary'}, status=400)
        try:
            url = Url.objects.get(short_url=short_url)
        except Url.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Url not found'}, status=404)
        return JsonResponse({'success': True, 'url': UrlSerializer(url).data}, status=400)


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