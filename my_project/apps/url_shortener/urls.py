from django.urls import path, include
from rest_framework.routers import DefaultRouter

from my_project.apps.url_shortener.views.url_shortener_views import UrlShortenerView, RedirectToUrl

router = DefaultRouter()
router.register(r"url_shortener", UrlShortenerView, basename='url_shortener')

urlpatterns = [
    path('', include(router.urls)),
    path('<str:short_url>/', RedirectToUrl.as_view(), name="redirect_to_url_api"),
]



