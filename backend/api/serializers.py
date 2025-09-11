from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, Transaction, Document

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = '__all__'

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    # Esto mostrará los detalles del comprador y vendedor, no solo su ID
    buyer = UserSerializer(read_only=True)
    seller = UserSerializer(read_only=True)
    documents = DocumentSerializer(many=True, read_only=True)  # Para incluir docs en la respuesta
    
    class Meta:
        model = Transaction
        fields = '__all__'