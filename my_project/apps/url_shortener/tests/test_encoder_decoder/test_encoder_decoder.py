import random
import string

from my_project.apps.url_shortener.encode_strategies.shake_256_hexdigest_strategy import Hex256HexdigestStrategy


class TestEncoderDecoder:

    def test_encode_no_collisions_with_small_set(self):
        enconding_strategy = Hex256HexdigestStrategy()
        used_hashes = {}
        used_random_string = {}
        collisions = 0
        for i in range(10000):
            random_string = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
            if used_random_string.get('random_string', None):
                continue
            else:
                used_random_string[random_string] = True
            url = 'www.testencode.com/'
            url += f'00000{i}/{random_string}'
            encoded = enconding_strategy.encode(url)
            already_used = used_hashes.get(encoded, None)
            if not already_used:
                used_hashes[encoded] = True
            else:
                collisions += 1
        assert collisions == 0

    def test_encode_no_collision_similar_long_urls(self):
        enconding_strategy = Hex256HexdigestStrategy()
        used_hashes = {}
        collisions = 0
        urls = [
            'www.google.com/some-test-long-text-to-try-collisions-in-long-strings',
            'www.google.com/some-test-long-text-to-try-collisions-in-long-string',
            'www.google.com/some-test-long-text-to-try-collisions-in-lon-strings',
            'www.google.com/some-test-long-texts-to-try-collisions-in-long-strings',
            'www.google.com/some-test-long-text-to-try-collisions-in-long-strings1',
            'www.google.com/some-test-longs-text-to-try-collisions-in-long-strings1',
        ]

        for url in urls:
            encoded = enconding_strategy.encode(url)
            already_used = used_hashes.get(encoded, None)
            if not already_used:
                used_hashes[encoded] = True
            else:
                collisions += 1
        assert collisions == 0

    def test_same_url_gives_same_encoded_value(self):
        url = 'www.google.com/some-test-same-url-gives-same-code'
        enconding_strategy = Hex256HexdigestStrategy()
        encoded = enconding_strategy.encode(url)
        re_encoded = enconding_strategy.encode(url)
        assert encoded == re_encoded
