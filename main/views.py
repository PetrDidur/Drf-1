from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from main.models import Course, Lesson, Payment, Subscription
from main.paginators import CoursePaginator
from main.permissions import IsModerator, IsOwner
from main.serializers import CourseSerializer, LessonSerializer, PaymentSerializer, SubscriptionSerializer

from rest_framework.filters import OrderingFilter


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
        subscription.course = Course.objects.get(pk=course_pk)
        subscription.save()


class SubscriptionDestroyAPIView(generics.DestroyAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]




