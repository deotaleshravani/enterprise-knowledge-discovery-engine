from django.urls import path

<<<<<<< HEAD
from search.views import (
    ExportAPIView,
    GraphAPIView,
    GraphSearchAPIView,
    GraphStatsAPIView,
    SearchExplanationAPIView,
)


urlpatterns = [
=======
from search.views import GraphAPIView


urlpatterns = [

>>>>>>> 295313f9544a55975afdff91c3cab55d8a5a635a
    path(
        "graph/",
        GraphAPIView.as_view(),
        name="graph",
    ),
<<<<<<< HEAD
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
=======

>>>>>>> 295313f9544a55975afdff91c3cab55d8a5a635a
]