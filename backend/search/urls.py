from django.urls import path

from search.views import (
    ExportAPIView,
    GraphAPIView,
    GraphSearchAPIView,
    GraphStatsAPIView,
    SearchExplanationAPIView,
)


urlpatterns = [
    path(
        "graph/",
        GraphAPIView.as_view(),
        name="graph",
    ),
    path(
        "graph/stats/",
        GraphStatsAPIView.as_view(),
        name="graph-stats",
    ),
    path(
        "graph/search/",
        GraphSearchAPIView.as_view(),
        name="graph-search",
    ),
    path(
        "search/explain/",
        SearchExplanationAPIView.as_view(),
        name="search-explain",
    ),
    path(
        "export/<str:file_format>/",
        ExportAPIView.as_view(),
        name="export-data",
    ),
]