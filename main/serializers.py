from datetime import date

from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.relations import SlugRelatedField

from main.models import Course, Lesson, Payment, Subscription
from main.services import create_and_save_link_to_pay
from main.validators import VideoLinkValidator


class LessonSerializer(serializers.ModelSerializer):
    course = SlugRelatedField(slug_field="name", queryset=Course.objects.all())

    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [VideoLinkValidator(field='video_link')]


class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField(read_only=True)
    lesson = LessonSerializer(many=True, read_only=True, source='lessons')
    is_subscribed = serializers.SerializerMethodField()
    payment_link = serializers.SerializerMethodField(read_only=True)

    def get_payment_link(self, course):
        user = self.context['request'].user
        current_date = date.today()
        Payment.objects.create(
            user=user,
            payment_date=current_date,
            course_or_lesson='course',
            payment_sum=course.price,
            payment_method='transfer'
        )
        return create_and_save_link_to_pay(course)

    def get_lessons_count(self, instance):
        return instance.lessons.count()

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Subscription.objects.filter(user=request.user, course=obj, is_active=True).exists()
        return False

    class Meta:
        model = Course
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'









