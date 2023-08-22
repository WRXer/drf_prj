import re

from rest_framework.exceptions import ValidationError


class UrlValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        tmp_val = dict(value).get(self.field)
        if tmp_val and not tmp_val.startswith('https://www.youtube.com/'):
            raise ValidationError("Прикрепление ссылок на сторонние ресурсы запрещено.")


class DesValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        tmp_val = dict(value).get(self.field)
        if tmp_val:
            # Ищем все ссылки в описании
            urls = re.findall(r'https?://\S+', tmp_val)
            for url in urls:
                if not url.startswith('https://www.youtube.com/'):
                    raise ValidationError("Прикрепление ссылок на сторонние ресурсы в описании запрещено.")