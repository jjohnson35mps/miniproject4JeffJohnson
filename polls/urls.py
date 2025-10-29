### INF601 - Advanced Programming in Python
### Jeff Johnson
### Mini Project 4

from django.urls import path
from . import views

app_name = "polls"

urlpatterns = [
    # Original poll pages
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),

    # College Football Playoff predictor pages
    path("cfp/vote/", views.cfp_vote, name="cfp_vote"),
    path("cfp/results/", views.cfp_results, name="cfp_results"),
]
