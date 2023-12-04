from django.urls import path

from main.apps import MainConfig
from rest_framework.routers import DefaultRouter

from main.views import CourseViewSet, LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView, \
    LessonUpdateAPIView, LessonDestroyAPIView, PaymentListAPIView, SubscriptionCreateAPIView, \
    SubscriptionDestroyAPIView, CoursePaymentAPIView

app_name = MainConfig.name


router = DefaultRouter()
router.register(r'course', CourseViewSet, basename='course')

urlpatterns = [
    path('lesson/create/', LessonCreateAPIView.as_view(), name='lesson-create'),
    path('lesson/', LessonListAPIView.as_view(), name='lesson-list'),
    path('lesson/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson-get'),
    path('lesson/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='lesson-update'),
    path('lesson/delete/<int:pk>/', LessonDestroyAPIView.as_view(), name='lesson-delete'),

    path('payment/', PaymentListAPIView.as_view(), name='payment_list'),
    path('course/<int:pk>/create_sub/', SubscriptionCreateAPIView.as_view(), name='subscription-create'),
    path('course/<int:pk>/delete_sub/', SubscriptionDestroyAPIView.as_view(), name='subscription-delete'),

    path('courses/<int:pk>/pay/', CoursePaymentAPIView.as_view(), name='course_pay')



] + router.urls
