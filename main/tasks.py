from celery import shared_task
from django.core.mail import send_mail

from django.conf import settings
from main.models import Course
from datetime import timedelta

from django.utils import timezone

from users.models import User


@shared_task
def send_update_course(course_id):
    try:
        course = Course.objects.get(pk=course_id)
        subject = f"Обновление курса: {course.name}"
        from_email = 'noreply@example.com'
        recipient_list = ['wrxwerrr@yandex.ru']    #course.subscribers.values_list('email', flat=True)
        send_mail(subject, from_email, settings.EMAIL_HOST_USER, recipient_list=recipient_list)
        print("Complete")
    except Course.DoesNotExist:
        print(f"Курс с id {course_id} не найден.")


@shared_task
def block_inactive_users():
    print('check users')
    one_month_ago = timezone.now() - timedelta(days=30)    # Находим дату, которая была месяц назад
    inactive_users = User.objects.filter(last_login__lte=one_month_ago, is_active=True)
    inactive_users.update(is_active=False)     # Блокируем пользователей, которые не входили в систему более месяца
    print('inactive users blocked')
