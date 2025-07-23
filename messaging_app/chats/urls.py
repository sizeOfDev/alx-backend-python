from rest_framework_nested import routers
from django.urls import path, include
from .views import ConversationViewSet, MessageViewSet, RegisterView

router = routers.DefaultRouter()

router.register(r'conversations', ConversationViewSet, basename='conversations')
conversations_router = routers.NestedDefaultRouter(router, r'conversations', lookup='conversation')
conversations_router.register(r'messages', MessageViewSet, basename='conversation-messages')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(conversations_router.urls)),
    path('register/', RegisterView.as_view(), name="Register")
]


