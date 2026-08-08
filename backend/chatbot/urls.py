from django.urls import path

from chatbot.views import (
    ChatAPIView,
    ChatHistoryAPIView,
)

urlpatterns = [

    path(
        "chat/",
        ChatAPIView.as_view(),
        name="chat",
    ),

    path(
        "chat/history/<uuid:session_id>/",
        ChatHistoryAPIView.as_view(),
        name="chat-history",
    ),

]