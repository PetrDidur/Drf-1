from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email="test1@mail.ru",
            first_name="test1",
            is_superuser=True,
            is_staff=False,
            is_active=True
        )

        user.set_password('9184')
        user.save()
