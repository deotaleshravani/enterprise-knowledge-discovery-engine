from django.urls import path

from search.views import GraphAPIView


urlpatterns = [

    path(
        "graph/",
        GraphAPIView.as_view(),
        name="graph",
    ),

]