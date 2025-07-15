from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework_simplejwt.tokens import RefreshToken


from .pagginations import MoviePagination
from users.serializers import *
from movieapp.models import *



__all__ = [
    "UserListAPIView",
    "UserRegisterAPIView",
    "LogInAPIView",
    "AccountDetailAPIView",
    "ChangePasswordAPIView",
    "UserLogoutAPIView",
]


class UserListAPIView(APIView):
    """APIView to list all users."""
    
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = MoviePagination  
    http_method_names = ["get"]
    
    @swagger_auto_schema(
        operation_description="Get list of all users (paginated)",
        responses={200: CustomUserSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        users = CustomUser.objects.all()  
        pagination = self.pagination_class()  
        result_page = pagination.paginate_queryset(users, request) 
        serializer = CustomUserSerializer(result_page, many=True)
        return pagination.get_paginated_response(serializer.data)


class UserRegisterAPIView(APIView):
    """APIView for user registration."""
    permission_classes = [AllowAny] 
    http_method_names = ["post"]
    
    @swagger_auto_schema(
        request_body=CustomUserRegisterSerializer,
        operation_description="Register a new user",
        responses={
            201: openapi.Response("Created", CustomUserRegisterSerializer),
            400: "Bad Request"
        }
    )
    def post(self, request, *args, **kwargs):
        """Handle POST requests to create a new user."""
        serializer = CustomUserRegisterSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save() 
            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "Profile created successfully",
                "username": user.username,
                "email": user.email,
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    
class LogInAPIView(APIView):
    """Users login APi method"""
    permission_classes = [AllowAny]
    http_method_names = ["post"]
    
    @swagger_auto_schema(
        request_body=LoginSerializer,
        operation_description="Login and get auth token",
        responses={
            200: openapi.Response("Login successful", schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(type=openapi.TYPE_STRING),
                    'token': openapi.Schema(type=openapi.TYPE_STRING)
                }
            )),
            400: "Invalid credentials"
        }
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "Login successful",
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class AccountDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "put"]
    
    @swagger_auto_schema(
        operation_description="Get your account info",
        responses={200: CustomUserSerializer()}
    )
    def get(self, request):
        serializer = CustomUserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=CustomUserSerializer,
        operation_description="Update your account info",
        responses={200: CustomUserSerializer(), 400: "Bad Request"}
    )
    def put(self, request):
        serializer = CustomUserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ["put"]

    @swagger_auto_schema(
        request_body=ChangePasswordSerializer,
        operation_description="Change your password",
        responses={
            200: openapi.Response("Password updated successfully"),
            400: "Validation Error"
        }
    )
    def put(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if not user.check_password(serializer.validated_data["old_password"]):
                return Response({"old_password": "Old password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(serializer.validated_data["new_password"])
            user.save()
            return Response({"message": "Password updated successfully"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserLogoutAPIView(APIView):
    """APIView for user logout."""
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    http_method_names = ["post"]

    @swagger_auto_schema(
        operation_description="Logout current user by deleting token",
        responses={
            200: openapi.Response("Logged out successfully"),
            400: "Invalid token"
        }
    )
    def post(self, request):
        """Handle POST requests to log out a user."""
        try:
            token = Token.objects.get(user=request.user)
            token.delete() 
            return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)