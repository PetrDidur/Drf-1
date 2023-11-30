import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from main.models import Lesson, Course, Subscription
from users.models import User


class LessonTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(
            email='admin@mail.ru',
            is_active=True
        )
        self.user.set_password('9184')
        self.user.save()

        get_token = reverse('user:token_obtain_pair')
        token_response = self.client.post(path=get_token, data={'email': 'admin@mail.ru', 'password': '9184'})
        token = token_response.json().get('access')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        self.headers = {'HTTP_AUTHORIZATION': f'Bearer {token}'}

        self.course = Course.objects.create(
            name='test_course',
            description='test'

        )

        self.lesson = Lesson.objects.create(
            name='test_lesson',
            course=self.course
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
                        "course": "test_course",
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
            "course": self.course,
                    }

        response = self.client.post(
            reverse('main:lesson-create'),
            data=data
        )
        print(response)

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            Lesson.objects.all().count(),
            2
        )

    def test_lesson_create_validation_error(self):

        data = {
            "name": "test",
            "course": self.course,
            "video_link": "wjw"
        }

        response = self.client.post(
            reverse('main:lesson-create'),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            response.json(),
            {'video_link': ['Enter a valid URL.']}

        )

    def test_retrieve_lesson(self):
        retrieve_url = reverse('main:lesson-get', args=[self.lesson.id])
        response = self.client.get(retrieve_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_lesson(self):
        update_url = reverse('main:lesson-update', args=[self.lesson.id])
        updated_data = {
            "name": "Updated Lesson",
            "description": "This is an updated lesson"
        }
        response = self.client.patch(update_url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.name, updated_data['name'])
        self.assertEqual(self.lesson.description, updated_data['description'])

    def test_delete_lesson(self):
        delete_url = reverse('main:lesson-delete', args=[self.lesson.id])
        response = self.client.delete(delete_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Lesson.objects.filter(id=self.lesson.id).exists())


class SubscriptionTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(
            email='admin@mail.ru',
            is_active=True
        )
        self.user.set_password('9184')
        self.user.save()

        get_token = reverse('user:token_obtain_pair')
        token_response = self.client.post(path=get_token, data={'email': 'admin@mail.ru', 'password': '9184'})
        token = token_response.json().get('access')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        self.headers = {'HTTP_AUTHORIZATION': f'Bearer {token}'}

        self.course = Course.objects.create(
            name='test_course',
            description='test_course',
            owner=self.user
        )

    def test_create(self):
        """Тестирование создания подписки"""
        subscription = {
            "user": self.user.pk,
            "course": self.course.pk
        }

        response = self.client.post(
            reverse('main:subscription-create', kwargs={'pk': self.course.pk}),
            data=subscription
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_delete(self):
        """Тестирование удаления подписки"""

        course = Subscription.objects.create(
            user=self.user,
            course=self.course
        )

        response = self.client.delete(
            reverse('main:subscription-delete', kwargs={'pk': course.pk})
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )







