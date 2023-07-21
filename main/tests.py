
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from main.models import Course, Lesson, Subscription
from users.models import User


# Create your tests here.


class MainTestCase(APITestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create_user(email='user@test.com', password='test')
        self.client.force_authenticate(user=self.user)  # Аутентифицируем клиента с созданным пользователем
        self.course = Course.objects.create(name="Test",preview="", description="test", owner= self.user)
        self.lesson = Lesson.objects.create(name="test",preview="", description="test", video_link="https://www.youtube.com/123fdsd", course=self.course)

    def test_create_course(self):
        """
        Тестирование создания курса
        """
        data = {
            "name": "Test",
            "preview": "",
            "description": "test",
            "owner": self.user.id
        }
        response = self.client.post(
            '/course/',
            data=data
        )
        #print(response.json())
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            response.json(),
            {'id': self.course.id + 1, 'lessons_count': 0, 'lessons': [], 'is_subscribed': False, 'name': 'Test', 'preview': None,
             'description': 'test', 'owner': self.user.id}
        )

        self.assertTrue(
            Course.objects.all().exists()
        )

    def test_create_lesson(self):
        """
        Тестирование создания урока
        """

        data = {
            "name": "test",
            "preview": "",
            "description": "test",
            "video_link": "https://www.youtube.com/123fdsd",
            "course": self.course.id
        }
        response = self.client.post(
            '/lesson/create/',
            data=data
        )
        #print(response.json())
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            response.json(),
            {'id': self.lesson.id + 1, 'name': 'test', 'description': 'test', 'preview': None,
             'video_link': 'https://www.youtube.com/123fdsd', 'course': self.course.id, 'owner': self.user.id}
        )

        self.assertTrue(
            Lesson.objects.all().exists()
        )
    def test_update_lesson(self):
        """
        Тестирование обновления урока
        """
        updated_lesson_data = {
            "name": "Updated Lesson",
            "preview": "",
            "description": "Updated Lesson Description",
            "video_link": "https://www.youtube.com/updated123",
            "course": self.course.id,
            "owner": self.user.id
        }
        update_url = f'/lesson/update/{self.lesson.id}/'  # Укажите правильный URL для обновления урока
        response = self.client.patch(update_url, data=updated_lesson_data)
        #print(response.json())
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {'id': self.lesson.id, 'name': 'Updated Lesson', 'description': 'Updated Lesson Description', 'preview': None,
             'video_link': 'https://www.youtube.com/updated123', 'course': self.course.id, 'owner': self.user.id}
        )

    def test_get_list(self):
        """
        Тестирование вывода списка уроков
        """
        response = self.client.get(
            reverse('main:lesson_list')
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_lesson_validation_error(self):
        """
        Тестирование урока на валидацию
        """
        data = {
            "name": "test",
            "preview": "",
            "description": "test",
            "video_link": "https://www.test.com/",
            "course": self.course.id
        }

        response = self.client.post(
            '/lesson/create/',
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )


    def test_subscribe(self):
        """
        Тестирование создания подписки на курс
        """
        data = {
            "user": self.user.id,
            "created_at": '',
            "course": self.course.id
        }
        url = f'/subscribe/{self.course.id}/'  # URL для создания подписки на курс
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        subscription = Subscription.objects.get(user=self.user, course=self.course)
        self.assertEqual(subscription.user.id, self.user.id)
        self.assertEqual(subscription.course.id, self.course.id)

    def test_unsubscribe(self):
        """
        Тестирование удаления подписки на курс
        """
        self.user.subscriptions.create(course=self.course)    # Создаем подписку для пользователя на курс
        url_from = f'/unsubscribe/{self.course.id}/'  # URL для удаления подписки на курс
        response = self.client.delete(url_from)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertFalse(self.user.subscriptions.filter(course=self.course).exists())
