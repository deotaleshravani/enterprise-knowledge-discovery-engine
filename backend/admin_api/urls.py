from django.urls import path

from admin_api.views import (
    DocumentStatsAPIView,
    ChunkStatsAPIView,
    SessionStatsAPIView,
    GraphStatsAPIView,
    SearchAnalyticsAPIView,
)
from admin_api.views import (
    DashboardStatisticsAPIView,
)
urlpatterns = [

    path(
        "documents/",
        DocumentStatsAPIView.as_view(),
    ),

    path(
        "chunks/",
        ChunkStatsAPIView.as_view(),
    ),

    path(
        "sessions/",
        SessionStatsAPIView.as_view(),
    ),

    path(
        "graph/",
        GraphStatsAPIView.as_view(),
    ),
    path(
        "dashboard/",
        DashboardStatisticsAPIView.as_view(),
    ),
    path(
        "analytics/",
        SearchAnalyticsAPIView.as_view(),
    ),

]