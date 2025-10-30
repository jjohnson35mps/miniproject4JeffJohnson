# ### INF601 - Advanced Programming in Python
# ### Jeff Johnson
# ### Mini Project 4

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from django.db.models import Count

# Auth (for registration/login support)
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import Question, Choice, ChampionshipPick

from django.contrib.auth import logout

# ---------------------------------
# Shared team list for CFP dropdown
# ---------------------------------
# Each item is (slug_key_used_in_form, human_readable_label)
TEAMS = [
    ("ohio_state", "Ohio State"),
    ("indiana", "Indiana"),
    ("texas_a_m", "Texas A&M"),
    ("alabama", "Alabama"),
    ("georgia", "Georgia"),
    ("oregon", "Oregon"),
    ("ole_miss", "Ole Miss"),
    ("georgia_tech", "Georgia Tech"),
    ("vanderbilt", "Vanderbilt"),
    ("byu", "BYU"),
    ("miami", "Miami"),
    ("notre_dame", "Notre Dame"),
    ("texas_tech", "Texas Tech"),
    ("tennessee", "Tennessee"),
    ("virginia", "Virginia"),
    ("louisville", "Louisville"),
    ("cincinnati", "Cincinnati"),
    ("oklahoma", "Oklahoma"),
    ("missouri", "Missouri"),
    ("texas", "Texas"),
    ("michigan", "Michigan"),
    ("houston", "Houston"),
    ("usc", "USC"),
    ("utah", "Utah"),
    ("memphis", "Memphis"),
]
# convenience map so we can go from "ohio_state" -> "Ohio State"
TEAM_LOOKUP = dict(TEAMS)


# -------------------------
# Landing / static-ish pages
# -------------------------

def home(request):
    """CFP-themed landing page (extends polls/base.html)."""
    return render(request, "polls/home.html")


def about(request):
    """About page."""
    return render(request, "polls/about.html")


def trivia(request):
    """College football trivia / fun facts."""
    facts = [
        "The first college football game was played in 1869 between Rutgers and Princeton.",
        "The College Football Playoff began with the 2014 season. Before that, the BCS picked the title matchup.",
        "Alabama under Nick Saban won six national titles between 2009 and 2020.",
        "Ohio State has multiple modern-era national championships and is regularly ranked in the AP Top 5.",
        "The Heisman Trophy has been awarded since 1935 to the most outstanding college football player.",
        "The AP Top 25 poll is voted on by sportswriters and broadcasters across the country.",
        "Notre Dame claims double-digit national championships and has produced multiple Heisman winners.",
        "The Rose Bowl, first played in 1902, is known as 'The Granddaddy of Them All'.",
        "The SEC has won the majority of national titles in the 21st century.",
        "BYU won a national title in 1984, going 13-0.",
    ]
    return render(request, "polls/trivia.html", {"facts": facts})


# -------------------------
# Registration (for rubric)
# -------------------------

def register(request):
    """
    Simple user registration using Django's built-in UserCreationForm.
    Templates expected:
      - templates/registration/register.html
      - (login/logout handled by contrib.auth URLs)
    """
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # log them in after signup
            return redirect("home")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {"form": form})


# -------------------------
# CFP Champion vote / results
# -------------------------

@require_http_methods(["GET", "POST"])
def cfp_vote(request):
    """
    Show the CFP vote form (GET) and handle submissions (POST).
    We store the *readable* team name in ChampionshipPick.team_name.
    """
    if request.method == "POST":
        picked_key = request.POST.get("team", "").strip()

        # validate it exists in TEAMS
        if picked_key in (k for k, _ in TEAMS):
            readable = TEAM_LOOKUP[picked_key]
            ChampionshipPick.objects.create(
                team_name=readable,
                voter=request.user if request.user.is_authenticated else None,
                voted_at=timezone.now(),
            )
            return redirect("polls:cfp_results")

        # invalid choice -> redisplay with error
        return render(
            request,
            "polls/cfp_vote.html",
            {"TEAMS": TEAMS, "error_message": "Please select a valid team."},
        )

    # GET
    return render(request, "polls/cfp_vote.html", {"TEAMS": TEAMS})


def cfp_results(request):
    """
    Aggregate ChampionshipPick rows by team_name and show counts (desc).
    """
    counts = (
        ChampionshipPick.objects.values("team_name")
        .annotate(total=Count("id"))
        .order_by("-total")
    )
    leaderboard = [{"team_name": row["team_name"], "count": row["total"]} for row in counts]

    return render(request, "polls/cfp_results.html", {"leaderboard": leaderboard})


# -------------------------
# Classic Polls (Django tutorial)
# -------------------------

class IndexView(generic.ListView):
    """
    Shows latest 5 poll Questions (not future-dated).
    Template: polls/index.html
    Context var: latest_question_list
    """
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        return (
            Question.objects.filter(pub_date__lte=timezone.now())
            .order_by("-pub_date")[:5]
        )


class DetailView(generic.DetailView):
    """Vote form for a single Question."""
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    """Results for a single Question."""
    model = Question
    template_name = "polls/results.html"


def vote(request, question_id):
    """
    Handle POST vote for a regular poll Question/Choice.
    """
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "polls/detail.html",
            {"question": question, "error_message": "You didn't select an answer."},
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))

def logout_then_home(request):
    """Log out on GET or POST, then send home."""
    logout(request)
    return redirect("home")