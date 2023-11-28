import re

from rest_framework.serializers import ValidationError


class VideoLinkValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        # Извлекаем значение по ключу из словаря
        tmp_val = value.get(self.field)

        if tmp_val:
            if 'https://www.youtube.com/' not in tmp_val:
                raise ValidationError('Разрешены только ссылки на youtube')





