from rest_framework import serializers
from .models import User,Question,Result


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'mobile', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            mobile=validated_data.get('mobile', '')
        )

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)



class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Question
        fields="__all__"


class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model=Result
        fields="__all__"

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=8, write_only=True)
    password2 = serializers.CharField(min_length=8, write_only=True, required=False)

    def validate(self, data):
        if data.get('password2') and data['password'] != data.get('password2'):
            raise serializers.ValidationError("Passwords do not match")
        return data