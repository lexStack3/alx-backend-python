from rest_framework import routers
from django.urls import path, include
from .views import ConversationViewSet, MessageViewSet

router = routers.DefaultRouter()
router.register('conversation', ConversationViewSet)
router.register('message', MessageViewSet)

urlpatterns = [
    path('', include(router.urls))
]
