import re

from rest_framework.serializers import ValidationError


class VideoLinkValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        youtube_pattern = re.compile(r'^https?://(?:www\.)?youtube\.com/watch\?v=[\w-]+')

        field_value = value.get(self.field)
        if field_value is not None and not youtube_pattern.match(field_value):
            raise ValidationError('youtube links are only allowed')




