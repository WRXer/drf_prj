from django.db import models


NULLABLE = {'blank': True, 'null': True}

# Create your models here.
class Course(models.Model):
    name = models.CharField(max_length=100)
    preview = models.ImageField(upload_to='previews/', verbose_name='превью курса', **NULLABLE)
    description = models.TextField()

    def __str__(self):
        return self.name


class Lesson(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    preview = models.ImageField(upload_to='lesson_previews/', verbose_name='превью урока', **NULLABLE)
    video_link = models.URLField()

    def __str__(self):
        return self.name