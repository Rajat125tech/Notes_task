from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import TaskViewSet, NoteViewSet, RegisterView, LogoutView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.authentication import JWTAuthentication

# -----------------------------
# Routers for Tasks & Notes
# -----------------------------
router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'notes', NoteViewSet, basename='note')

# -----------------------------
# Swagger Schema Configuration
# -----------------------------
schema_view = get_schema_view(
    openapi.Info(
        title="Tasks & Notes API",
        default_version='v1',
        description="API for managing tasks and notes with JWT authentication",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    authentication_classes=(JWTAuthentication,),
)

# ✅ Add Bearer Token Authorization to Swagger
schema_view.security_definitions = {
    'Bearer': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': 'JWT Authorization header using the Bearer scheme. Example: "Bearer <your_token>"',
    }
}
schema_view.security = [{'Bearer': []}]

# -----------------------------
# URL Patterns
# -----------------------------
urlpatterns = [
    # CRUD endpoints
    path('', include(router.urls)),

    # Authentication endpoints
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),

    # Swagger Docs
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
