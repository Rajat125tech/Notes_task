from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers # 🌟 ADDED IMPORT
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Task, Note
from .serializers import TaskSerializer, NoteSerializer, UserSerializer


# ----------------------------
# LOGOUT SERIALIZER (New)
# ----------------------------
class RefreshTokenSerializer(serializers.Serializer):
    """Serializer to explicitly define the required input for logout."""
    refresh = serializers.CharField(required=True, help_text="The Refresh Token to blacklist.")


# ----------------------------
# USER REGISTRATION VIEW
# ----------------------------
class RegisterView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Register a new user and get JWT tokens.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["username", "password"],
            properties={
                "username": openapi.Schema(type=openapi.TYPE_STRING, description="Username"),
                "password": openapi.Schema(type=openapi.TYPE_STRING, description="Password"),
            },
        ),
        responses={
            201: openapi.Response(description="User registered successfully"),
            400: openapi.Response(description="Invalid input or user already exists"),
        },
    )
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "Username and password required"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password)
        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)

        return Response(
            {
                "message": "User registered successfully",
                "user": {"id": user.id, "username": user.username},
                "tokens": {"refresh": str(refresh), "access": access},
            },
            status=status.HTTP_201_CREATED,
        )


# ----------------------------
# TASK VIEWSET
# ----------------------------
class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # ✅ Prevent Swagger & anonymous user crashes
        if getattr(self, 'swagger_fake_view', False) or self.request.user.is_anonymous:
            return Task.objects.none()
        return Task.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def mark_complete(self, request, pk=None):
        task = self.get_object()
        task.completed = True
        task.save()
        return Response({'status': 'marked complete'})


# ----------------------------
# NOTE VIEWSET
# ----------------------------
class NoteViewSet(viewsets.ModelViewSet):
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # ✅ Prevent Swagger & anonymous user crashes
        if getattr(self, 'swagger_fake_view', False) or self.request.user.is_anonymous:
            return Note.objects.none()
        return Note.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        task = serializer.validated_data.get('task')
        if task.user != self.request.user:
            return Response({'detail': 'Task does not belong to user'}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save(user=self.request.user)


# ----------------------------
# LOGOUT VIEW
# ----------------------------
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Blacklist the provided Refresh Token to log out the user. Requires a valid Access Token in the Authorization header.",
        request_body=RefreshTokenSerializer, # 🌟 Reference to the new serializer
        responses={
            205: openapi.Response(description="Logout successful (Token blacklisted)"),
            400: openapi.Response(description="Invalid refresh token or missing 'refresh' field"),
        },
        security=[{'Bearer': []}]
    )
    def post(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response({"error": "Refresh token required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
