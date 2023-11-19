from rest_framework import serializers

from main.serializers import PaymentSerializer
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    payment = PaymentSerializer(read_only=True, many=True, source='payments')

    class Meta:
        model = User
        fields = '__all__'
