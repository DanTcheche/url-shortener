import hashlib

from my_project.apps.url_shortener.encode_strategies.encode_strategy import EncodeStrategy


class Hex256HexdigestStrategy(EncodeStrategy):

    def encode(self, text):
        return hashlib.shake_256(text.encode()).hexdigest(5)
