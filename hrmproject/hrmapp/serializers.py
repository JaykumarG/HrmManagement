from rest_framework import serializers
from .models import User, Company

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name', 'domain']


class UserRegisterSerializer(serializers.ModelSerializer):
    company = serializers.SlugRelatedField(
        slug_field='domain', queryset=Company.objects.all()
    )

    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'company', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        company = validated_data.pop('company')
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, company=company, **validated_data)
        return user
