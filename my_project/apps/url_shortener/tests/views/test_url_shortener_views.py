import pytest
from rest_framework.test import APIClient

from my_project.apps.url_shortener.models import Url


@pytest.mark.django_db
class TestUrlShortenerAPI:

    @pytest.fixture
    def set_up(self):
        self.client = APIClient()
        self.url = 'https://test-url.com'

    def test_encode(self, set_up):
        params = {
            'long_url': self.url
        }
        response = self.client.post('/url_shortener/encode/', params)

        assert response.status_code == 200, str(response.content)
        response = response.json()
        assert response['success']
        assert response['url']['long_url'] == self.url
        assert Url.objects.all().count() == 1

    def test_re_encode_doesnt_create_new_url(self, set_up):
        params = {
            'long_url': self.url
        }
        self.client.post('/url_shortener/encode/', params)

        response = self.client.post('/url_shortener/encode/', params)

        assert response.status_code == 200, str(response.content)
        assert Url.objects.all().count() == 1

    def test_no_long_url_returns_400(self, set_up):
        response = self.client.post('/url_shortener/encode/')

        assert response.status_code == 400, str(response.content)
        assert response.json()['message'] == 'Long url is necessary'
        assert Url.objects.all().count() == 0

    def test_encode_wrong_url(self, set_up):
        params = {
            'long_url': 'sometextnoturl.asd'
        }
        self.client.post('/url_shortener/encode/', params)

        response = self.client.post('/url_shortener/encode/', params)

        assert response.status_code == 400, str(response.content)
        assert response.json()['message'] == 'Url is incorrect, make sure it complies ' \
                                             'to the following format. http(s)://'

    def test_decode(self, set_up):
        url = Url.objects.create(long_url=self.url)
        params = {
            'short_url': url.short_url
        }
        response = self.client.post('/url_shortener/decode/', params)
        assert response.status_code == 200, str(response.content)
        response = response.json()
        assert response['url']['long_url'] == self.url

    def test_decode_not_existing_url(self, set_up):
        params = {
            'short_url': 'notexisting'
        }
        response = self.client.post('/url_shortener/decode/', params)
        assert response.status_code == 404, str(response.content)
        assert response.json()['message'] == 'Url not found'

    def test_no_short_url_returns_400(self, set_up):
        response = self.client.post('/url_shortener/decode/')

        assert response.status_code == 400, str(response.content)
        assert response.json()['message'] == 'Short url is necessary'
