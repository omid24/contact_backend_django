from django.contrib.auth import get_user_model
from rest_framework import serializers
from contacts.models import Contact


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'first_name', 'last_name', 'username', 'phone_number', 'image', 'password')


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('id', 'first_name', 'last_name', 'phone_number', 'image',)


class ContactImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('image',)
