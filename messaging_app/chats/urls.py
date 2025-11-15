from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import ConversationViewSet, MessageViewSet

router = DefaultRouter()
router.register('conversation', ConversationViewSet)
router.register('message', MessageViewSet)

urlpatterns = [
    path('', include(router.urls))
]
