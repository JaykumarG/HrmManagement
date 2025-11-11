from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserRegisterSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import UserRegisterSerializer, CompanySerializer
from .auth_serializers import CompanyTokenObtainSerializer
from .models import Company

class RegisterAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """
        Register a user. Request must provide:
        {
          "email": "...",
          "full_name": "...",
          "password": "...",
          "company": "company-domain.example"   # slug domain
        }
        """
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Return tokens on registration
            from rest_framework_simplejwt.tokens import RefreshToken
            refresh = RefreshToken.for_user(user)
            return Response({
                "user_id": user.id,
                "email": user.email,
                "full_name": user.full_name,
                "company": user.company.domain,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """
        Login with email + password + company(domain)
        {
           "email": "...",
           "password": "...",
           "company": "company-domain.example"
        }
        """
        serializer = CompanyTokenObtainSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

