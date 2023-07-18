from django.conf import settings
from django.db import models
from datetime import date
from users.models import User


NULLABLE = {'blank': True, 'null': True}

# Create your models here.
class Course(models.Model):
    name = models.CharField(max_length=100)
    preview = models.ImageField(upload_to='previews/', verbose_name='превью курса', **NULLABLE)
    description = models.TextField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class Lesson(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    preview = models.ImageField(upload_to='lesson_previews/', verbose_name='превью урока', **NULLABLE)
    video_link = models.URLField()
    course = models.ForeignKey(Course, default=1, on_delete=models.CASCADE, related_name='lessons')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class Payment(models.Model):
    payment_method_choices = [
        ('cash', 'Наличные'),
        ('transfer', 'Перевод на счет')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    payment_date = models.DateField(default=date.today)
    paid_course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    paid_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, null=True, blank=True)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=payment_method_choices)

    def __str__(self):
        return f"Платеж по {self.paid_course if self.paid_course else self.paid_lesson}"

    class Meta:
        ordering = ("-id",)