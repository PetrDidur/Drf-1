import re

from rest_framework.serializers import ValidationError


class VideoLinkValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        reg = re.compile(r'^https?://(?:www\.)?youtube\.com/.+$')
        tmp_val = dict(value).get(self.field)
        if not bool(reg.match(tmp_val)):
            raise ValidationError('Not ok')
        if 'youtube.com' not in tmp_val:
            raise ValidationError('Разрешены только ссылки на youtube')

