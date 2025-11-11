from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model
from .models import Company

User = get_user_model()

class CompanyTokenObtainSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    company = serializers.CharField(help_text="company domain (e.g., test.myhrm.com)")

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        company_domain = attrs.get("company")

        # find company
        try:
            company = Company.objects.get(domain=company_domain)
        except Company.DoesNotExist:
            raise serializers.ValidationError({"company": "Company with this domain does not exist."})

        # find user under company
        try:
            user = User.objects.get(email__iexact=email, company=company)
        except User.DoesNotExist:
            raise serializers.ValidationError({"detail": "No account found for this email under the given company."})

        if not user.check_password(password):
            raise serializers.ValidationError({"detail": "Invalid credentials."})

        if not user.is_active:
            raise serializers.ValidationError({"detail": "User account disabled."})

        # Attach tokens using SimpleJWT programmatically
        from rest_framework_simplejwt.tokens import RefreshToken
        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user_id": user.id,
            "email": user.email,
            "full_name": getattr(user, "full_name", ""),
            "company": company.domain,
            "role": getattr(user, "role", "")
        }
