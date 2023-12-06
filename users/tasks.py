from celery import shared_task
from django.utils import timezone

from users.models import User
from celery.utils.log import get_task_logger, logger


@shared_task
def block_inactive_users():
    logger.info("function started")
    # Определяем период неактивности (в данном случае, 30 дней)
    inactive_period = timezone.now() - timezone.timedelta(days=30)

    # Находим пользователей, не входивших в систему более месяца
    inactive_users = User.objects.filter(last_login__lt=inactive_period, is_active=True)
    inactive_users.update(is_active=False)
    inactive_users.save()
    logger.info("function ended")


