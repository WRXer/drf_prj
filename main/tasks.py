from celery import shared_task
from django.core.mail import send_mail

from django.conf import settings
from main.models import Course


@shared_task
def example_task():
    print('Пример выполнения задачи!')
    # Ваши действия здесь


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

