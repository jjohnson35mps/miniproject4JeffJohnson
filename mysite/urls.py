"""mysite URL Configuration

Jeff Johnson
INF XXX - Mini Project Four (Django CFP Predictor App)
"""

from django.contrib import admin
from django.urls import include, path
from polls import views as polls_views  # import views from polls for home/about

urlpatterns = [
    # Root landing page
    path("", polls_views.home, name="home"),

    # About page (project explainer / satisfies extra page requirement)
    path("about/", polls_views.about, name="about"),

    # Polls app URLs (poll list, detail, etc., + CFP vote/results)
    path("polls/", include("polls.urls")),

    # Admin site (login required)
    path("admin/", admin.site.urls),

    path("trivia/", polls_views.trivia, name="trivia"),

]
