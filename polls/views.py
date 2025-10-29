### INF601 - Advanced Programming in Python
### Jeff Johnson
### Mini Project 4

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from django.db.models import Count

from .models import Question, Choice, ChampionshipPick


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
    """
    Home page. Introduces the CFP prediction vote and links to everything.
    Extends polls/base.html with CFP theme.
    """
    return render(request, "polls/home.html")


def about(request):
    """
    About page. Explains what this project is for class.
    """
    return render(request, "polls/about.html")


def trivia(request):
    """
    College football trivia / fun facts page.
    Sent to template so we can loop and pretty-print.
    """
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
# CFP Champion vote / results
# -------------------------

@require_http_methods(["GET", "POST"])
def cfp_vote(request):
    """
    Show the CFP vote form (GET) and handle submissions (POST).

    Template: polls/cfp_vote.html (extends polls/base.html)

    Important:
    - Your real model fields are team_name (CharField), voter (FK or None),
      voted_at (DateTimeField).
    - We save the *human-readable* team ("Ohio State"), not the slug key.
    """

    if request.method == "POST":
        picked_key = request.POST.get("team", "").strip()

        # make sure it's a valid option from TEAMS
        valid_keys = [key for (key, _label) in TEAMS]
        if picked_key in valid_keys:
            readable_name = TEAM_LOOKUP[picked_key]  # e.g. "Ohio State"

            ChampionshipPick.objects.create(
                team_name=readable_name,
                voter=request.user if request.user.is_authenticated else None,
                voted_at=timezone.now(),
            )

            return redirect("polls:cfp_results")

        # invalid or missing pick -> re-render with error
        return render(
            request,
            "polls/cfp_vote.html",
            {
                "TEAMS": TEAMS,
                "error_message": "Please select a valid team.",
            },
        )

    # GET request: just render blank form
    return render(
        request,
        "polls/cfp_vote.html",
        {
            "TEAMS": TEAMS,
        },
    )


def cfp_results(request):
    """
    Leaderboard page.

    We aggregate ChampionshipPick rows by team_name and count them.
    We DO NOT group by the slug key because the DB only knows team_name.
    """

    # SELECT team_name, COUNT(*) AS total
    # FROM polls_championshippick
    # GROUP BY team_name
    # ORDER BY total DESC;
    counts = (
        ChampionshipPick.objects
        .values("team_name")
        .annotate(total=Count("id"))
        .order_by("-total")
    )

    # massage into something easy for the template
    leaderboard = []
    for row in counts:
        leaderboard.append({
            "team_name": row["team_name"],
            "count": row["total"],
        })

    return render(
        request,
        "polls/cfp_results.html",
        {
            "leaderboard": leaderboard,
        },
    )


# -------------------------
# Classic Polls (Django tutorial)
# -------------------------

class IndexView(generic.ListView):
    """
    Shows latest 5 poll Questions (not future-dated).
    Template: polls/index.html  (extends polls/base.html in our project)
    Context var: latest_question_list
    """
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        return (
            Question.objects
            .filter(pub_date__lte=timezone.now())
            .order_by("-pub_date")[:5]
        )


class DetailView(generic.DetailView):
    """
    Detail page for a single Question (vote form).
    Template: polls/detail.html
    """
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        # Don't show questions scheduled in the future.
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    """
    Shows results for a single Question (tally of each Choice).
    Template: polls/results.html
    """
    model = Question
    template_name = "polls/results.html"


def vote(request, question_id):
    """
    Handle POST vote for a regular poll Question/Choice.
    After saving, redirect back to that Question's results page.
    If no choice provided, redisplay form with an error.
    """
    question = get_object_or_404(Question, pk=question_id)

    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the voting form with an error message.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select an answer.",
            },
        )
    else:
        selected_choice.votes = selected_choice.votes + 1
        selected_choice.save()
        return HttpResponseRedirect(
            reverse("polls:results", args=(question.id,))
        )
