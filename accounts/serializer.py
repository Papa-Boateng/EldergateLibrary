from rest_framework import serializers
from .models import Administrator, Librarian, Reader


class AdministratorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Administrator
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }


class LibrarianSerializer(serializers.ModelSerializer):
    class Meta:
        model = Librarian
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }


class ReaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reader
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }