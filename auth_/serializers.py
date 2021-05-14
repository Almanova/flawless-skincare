from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from rest_framework import serializers

from mixin.serializers import BaseModelSerializer
from .models import User
from utils import constants
from utils.tokens import token_generator


class UserUpdateSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    phone = serializers.CharField(max_length=50)

    def update(self, instance, validated_data):
        if validated_data.get('email') != instance.email:
            instance.confirmed = False
            instance.email = validated_data.get('email', instance.email)
            RegistrationSerializer.send_confirmation_email(instance)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.save()
        return instance


class UserSerializer(UserUpdateSerializer):
    id = serializers.IntegerField(read_only=True)
    is_active = serializers.BooleanField()
    is_staff = serializers.BooleanField()
    role = serializers.CharField(max_length=30)
    confirmed = serializers.BooleanField()


class RegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    email = serializers.EmailField(max_length=100)
    role = serializers.CharField(max_length=30, required=False)
    password = serializers.CharField(max_length=128)

    def register(self):
        user = User.objects.create_user(username=self.validated_data['username'],
                                        email=self.validated_data['email'],
                                        role=self.validated_data
                                        .get('role', constants.CUSTOMER))
        user.set_password(self.validated_data['password'])
        user.save()
        self.send_confirmation_email(user)
        return user

    @staticmethod
    def send_confirmation_email(user):
        subject = 'Confirm your email for Flawless Skincare account'
        uid = urlsafe_base64_encode(force_bytes(user.id))
        link = settings.API_URL + "/auth/confirm/?uid={}&token={}"\
            .format(uid, token_generator.make_token(user))
        html_content = render_to_string(
            'confirmation_email.html',
            {
                'user': user,
                'link': link
            }
        )
        text_content = strip_tags(html_content)
        send_mail(subject, text_content, settings.EMAIL_HOST_USER,
                  [user.email], html_message=html_content)


class ConfirmationSerializer(serializers.Serializer):
    uid = serializers.CharField(max_length=100)
    token = serializers.CharField(max_length=200)

    def confirm(self):
        try:
            uid = urlsafe_base64_decode(self.validated_data['uid'])
            user = User.objects.get(id=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            return False
        if token_generator.check_token(user, self.validated_data['token']):
            user.confirmed = True
            user.save()
            return True
        return False


class CustomerProfileSerializer(BaseModelSerializer):
    id = serializers.IntegerField(read_only=True)
    user = UserSerializer(read_only=True)
    city = serializers.CharField(max_length=50)
    address = serializers.CharField(max_length=200)
    birth_date = serializers.DateField()
    avatar = serializers.FileField(required=False)

    def update(self, instance, validated_data):
        instance.city = validated_data.get('city', instance.city)
        instance.address = validated_data.get('address', instance.address)
        instance.birth_date = validated_data.get('birth_date', instance.birth_date)
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.save()
        return instance


class AdminProfileSerializer(CustomerProfileSerializer):
    position = serializers.CharField(max_length=100)

    def update(self, instance, validated_data):
        instance.position = validated_data.get('position', instance.position)
        return super().update(instance, validated_data)


class BrandSerializer(BaseModelSerializer):
    id = serializers.IntegerField(read_only=True)
    user = UserSerializer(read_only=True)
    name = serializers.CharField(max_length=100)
    logo = serializers.FileField(required=False)
    description = serializers.CharField(max_length=500, required=False)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.logo = validated_data.get('logo', instance.logo)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance
