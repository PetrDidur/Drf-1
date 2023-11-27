import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from main.models import Lesson, Course
from users.models import User


class LessonTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(
            email='test@mail.ru',
            is_active=True
        )
        self.user.set_password('9184')
        self.user.save()

        get_token = reverse('user:token_obtain_pair')
        token_response = self.client.post(path=get_token, data={'email': 'test@mail.ru', 'password': '9184'})
        token = token_response.json().get('access')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        self.headers = {'HTTP_AUTHORIZATION': f'Bearer {token}'}

        self.course = Course.objects.create(
            name='test_course',
            description='test'
        )

        self.lesson = Lesson.objects.create(
            name='test_lesson',
        )

    def test_get_list(self):
        """Test for getting list of lessons"""

        response = self.client.get(
            reverse('main:lesson-list')
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": self.lesson.id,
                        "course": self.lesson.course_id,
                        "name": self.lesson.name,
                        "description": self.lesson.description,
                        "preview": None,
                        "video_link": None,
                        "owner": self.lesson.owner_id
                    }
                ]
            }

        )

    def test_lesson_create(self):
        """Test lesson creating"""

        data = {
                        "name": "test",
                    }

        response = self.client.post(
            reverse('main:lesson-create'),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )


