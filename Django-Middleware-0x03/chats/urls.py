from rest_framework_nested import routers
from django.urls import path, include
from .views import ConversationViewSet, MessageViewSet
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

router = routers.DefaultRouter()
router.register('conversation', ConversationViewSet, basename='conversation')

conversation_router = routers.NestedDefaultRouter(router, r'conversation',
                                                  lookup='conversation')
conversation_router.register(r'messages', MessageViewSet,
                             basename='conversation-messages')

schema_view = get_schema_view(
    openapi.Info(
        title='Messaging App API',
        default_version='v1',
        description='API documentation for Messaging App',
        terms_of_service='https://www.localhost.com/terms/',
        contact=openapi.Contact(email='alexanderedim80@gmail.com'),
        license=openapi.License(name='MIT License')
    ),
    public=True,
    permission_classes=(permissions.AllowAny,)
)

urlpatterns = [
    path('', include(router.urls)),
    path('', include(conversation_router.urls)),

    # Swagger endpoints
    path('swagger.json', schema_view.without_ui(cache_timeout=0),
         name='schema-json'),
    path('swagger', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('redoc', schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),

    # JWT Auth endpoints
    path('auth/login', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('auth/refresh', TokenRefreshView.as_view(),
         name='token_refresh')
]
