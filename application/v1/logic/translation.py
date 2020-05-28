from application.v1.model.translations import Translations


class Translation:

    def __init__(self, **kwargs):
        self._spanish_word = kwargs.get('spanish')
        self._english_word = kwargs.get('english')
        self._translations = Translations()

    def tranlate(self, direction):
        return self._get_spanish() if direction == 'spanish-english' else self._get_english()

    def _get_english(self):
        word = self._translations.translate_english(self._english_word);
        return word.get('spanish', None);

    def _get_spanish(self):
        palabra = self._translations.translate_spanish(self._spanish_word);
        return palabra.get('english', None);
