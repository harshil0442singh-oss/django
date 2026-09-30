from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny

from .serializers import (
    RecruiterSignupSerializer, SeekerSignupSerializer,
    LoginSerializer, RecruiterProfileSerializer, SeekerProfileSerializer
)
from .permissions import IsRecruiter, IsSeeker


class RecruiterSignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RecruiterSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Your account has been created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SeekerSignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SeekerSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Your account has been created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        request.user.auth_token.delete()
        return Response({"message": "You've been logged out successfully"}, status=status.HTTP_200_OK)


class RecruiterProfileView(APIView):
    permission_classes = [IsAuthenticated, IsRecruiter]

    def get(self, request):
        serializer = RecruiterProfileSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request):
        serializer = RecruiterProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        request.user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SeekerProfileView(APIView):
    permission_classes = [IsAuthenticated, IsSeeker]

    def get(self, request):
        serializer = SeekerProfileSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request):
        serializer = SeekerProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        request.user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
