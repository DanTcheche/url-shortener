import pytest
from rest_framework.test import APIClient

from my_project.apps.url_shortener.models import Url


@pytest.mark.django_db
class TestUrlRedirectAPI:

    @pytest.fixture
    def set_up(self):
        self.client = APIClient()
        self.url = 'https://www.test-url.com'

    def test_redirect(self, set_up):
        url = Url.objects.create(long_url=self.url)
        response = self.client.get(f'/{url.short_url}')
        assert response.status_code == 301, str(response.content)
