import pytest
from unittest import mock
from django.core.exceptions import ValidationError
from my_project.apps.url_shortener.models import Url


@pytest.mark.django_db
class TestCreateUrl:

    @pytest.fixture
    def set_up(self):
        self.existing_url = Url.objects.create(long_url='https://www.correcturl.com')

    def test_create_url_with_valid_url(self):
        url = Url.objects.create(long_url='https://www.correcturl.com')
        assert url.short_url is not None

    def test_create_url_with_invalid_url(self):
        with pytest.raises(ValidationError):
            Url.objects.create(long_url='asdf')
        assert Url.objects.all().count() == 0

    @mock.patch.object(Url, 'clean')
    def test_modify_times_visited_does_not_re_encode(self, mock_clean, set_up):
        self.existing_url.times_visited += 1
        self.existing_url.save()
        assert not mock_clean.called
        self.existing_url.long_url = 'https://www.correcturl.com'
        self.existing_url.save()
        assert not mock_clean.called
        self.existing_url.long_url = 'https://www.anothercorrecturl.com'
        self.existing_url.save()
        assert mock_clean.called
