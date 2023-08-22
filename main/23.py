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
    print(response.json())
    self.assertEqual(
        response.status_code,
        status.HTTP_201_CREATED
    )

    self.assertEqual(
        response.json(),
        {'id': 1, 'name': 'test', 'description': 'test', 'preview': None,
         'video_link': 'https://www.youtube.com/123fdsd', 'course': 2, 'owner': 2}
    )

    self.assertTrue(
        Lesson.objects.all().exists()
    )


def test_update_lesson(self):
    """
    Тестирование обновления урока
    """
    # Создаем курс, чтобы использовать его в создании урока
    course_data = {
        "name": "Test Course",
        "preview": "",
        "description": "Test Description",
        "owner": self.user.id
    }
    course_response = self.client.post('/course/', data=course_data)
    course_id = course_response.json()['id']

    # Создаем урок и связываем его с созданным курсом
    lesson_data = {
        "name": "Test Lesson",
        "preview": "",
        "description": "Test Lesson Description",
        "video_link": "https://www.youtube.com/123fdsd",
        "course": course_id
    }
    lesson_response = self.client.post('/lesson/create/', data=lesson_data)
    lesson_id = lesson_response.json()['id']

    # Обновляем урок
    updated_lesson_data = {
        "name": "Updated Lesson",
        "preview": "",
        "description": "Updated Lesson Description",
        "video_link": "https://www.youtube.com/updated123",
        "course": course_id
    }
    update_url = f'/lesson/update/{lesson_id}/'  # Укажите правильный URL для обновления урока
    response = self.client.patch(update_url, data=updated_lesson_data)
    # print(response.json())
    self.assertEqual(
        response.status_code,
        status.HTTP_200_OK
    )