### INF601 - Advanced Programming in Python
### Jeff Johnson
### Mini Project 4

from django.urls import path
from . import views

app_name = "polls"

urlpatterns = [
    # Home / landing page (CFP predictor hub)
    path("", views.home, name="home"),

    # About / info pages
    path("about/", views.about, name="about"),
    path("trivia/", views.trivia, name="trivia"),

    # Classic poll pages (college football opinion polls)
    # We mount these at /polls/ so they feel like a sub-section
    path("polls/", views.IndexView.as_view(), name="index"),
    path("polls/<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("polls/<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("polls/<int:question_id>/vote/", views.vote, name="vote"),

    # College Football Playoff predictor pages
    path("cfp/vote/", views.cfp_vote, name="cfp_vote"),
    path("cfp/results/", views.cfp_results, name="cfp_results"),
]
