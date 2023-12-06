from django.conf import settings
from django.shortcuts import render
from django.views import View
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from config.settings import STRIPE_SECRET_KEY
from main.models import Course, Lesson, Payment, Subscription
from main.paginators import CoursePaginator
from main.permissions import IsModerator, IsOwner
from main.serializers import CourseSerializer, LessonSerializer, PaymentSerializer, SubscriptionSerializer

from rest_framework.filters import OrderingFilter

from main.tasks import send_emails


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = CoursePaginator

    """def get_permissions(self):
        permission_classes = [IsAuthenticated, IsOwner | IsModerator]
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        if self.action == 'retrieve' or self.action == 'list':
            permission_classes = [IsAuthenticated, IsModerator | IsOwner]
        if self.action == 'destroy':
            permission_classes = [IsAuthenticated, IsOwner]
        if self.action == 'update':
            permission_classes = [IsAuthenticated, IsModerator, IsOwner]
        return [permission() for permission in permission_classes]"""

    def perform_create(self, serializer):
        new_course = serializer.save()
        new_course.owner = self.request.user
        new_course.save()

    def perform_update(self, serializer):
        serializer.save()
        pk = self.kwargs.get('pk')
        course = Course.objects.get(pk=pk)
        subscriptions = Subscription.objects.filter(course=course, is_active=True)
        subject = 'Course update'
        message = 'Course update'
        from_email = settings.EMAIL_HOST_USER

        emails = list(subscriptions.values_list('user__email', flat=True))

        send_emails.delay(emails, subject, message, from_email)
        return Response('Message sent')


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer

    # permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    # permission_classes = [IsAuthenticated]
    pagination_class = CoursePaginator


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    # permission_classes = [IsAuthenticated, IsOwner | IsModerator]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    # permission_classes = [IsAuthenticated, IsOwner | IsModerator]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    # permission_classes = [IsAuthenticated, IsOwner]


class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    # permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('course_or_lesson', 'payment_method',)
    ordering_fields = ('payment_date',)


class SubscriptionCreateAPIView(generics.CreateAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    def perform_create(self, serializer, *args, **kwargs):
        subscription = serializer.save()  # получаю подписку
        subscription.user = self.request.user  # сохраняю в базе юзера
        course_pk = self.kwargs.get('pk')  # сохраняю pk
        subscription.course = Course.objects.get(pk=course_pk)  # достаю нужную подписку
        subscription.save()


class SubscriptionDestroyAPIView(generics.DestroyAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]


class CoursePaymentAPIView(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, context={'request': request})
        payment_link = serializer.data['payment_link']
        return Response({'payment_link': payment_link})




























