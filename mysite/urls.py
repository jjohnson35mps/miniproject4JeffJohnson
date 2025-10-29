# ### INF601 - Advanced Programming in Python
# ### Jeff Johnson
# ### Mini Project 4

from django.contrib import admin
from django.urls import include, path
from polls import views as polls_views  # home/about/trivia/register/logout

urlpatterns = [
    # Root landing page -> CFP home
    path("", polls_views.home, name="home"),

    # Extra pages
    path("about/", polls_views.about, name="about"),
    path("trivia/", polls_views.trivia, name="trivia"),

    # Polls app (classic polls + CFP routes inside polls/urls.py)
    path("polls/", include(("polls.urls", "polls"), namespace="polls")),

    # Admin
    path("admin/", admin.site.urls),

    # Auth (built-in) + Register
    # IMPORTANT: put custom logout BEFORE the auth include so it takes precedence
    path("accounts/logout/", polls_views.logout_then_home, name="logout"),
    path("accounts/register/", polls_views.register, name="register"),
    path("accounts/", include("django.contrib.auth.urls")),  # login/password reset/change, etc.
]
