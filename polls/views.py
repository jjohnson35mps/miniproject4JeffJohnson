### INF601 - Advanced Programming in Python
### Jeff Johnson
### Mini Project 4

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from django.db.models import Count

from .models import Question, Choice, ChampionshipPick


# -------------------------
# Landing / static-ish pages
# -------------------------

def home(request):
    """
    Home page. Introduces the CFP prediction vote and links to everything.
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
# CFP Champion vote
# -------------------------

# Snapshot of the AP Top 25 teams we’re letting people pick from.
# You can tweak this list if the rankings change.
AP_TOP_25 = [
    "Ohio State",
    "Indiana",
    "Texas A&M",
    "Alabama",
    "Georgia",
    "Oregon",
    "Ole Miss",
    "Georgia Tech",
    "Vanderbilt",
    "BYU",
    "Miami",
    "Notre Dame",
    "Texas Tech",
    "Tennessee",
    "Virginia",
    "Louisville",
    "Cincinnati",
    "Oklahoma",
    "Missouri",
    "Texas",
    "Michigan",
    "Houston",
    "USC",
    "Utah",
    "Memphis",
]

@require_http_methods(["GET", "POST"])
def cfp_vote(request):
    """
    Show the CFP vote form and handle POST submissions.
    Saves a ChampionshipPick row with the chosen team.
    """
    if request.method == "POST":
        picked_team = request.POST.get("team_choice")

        # Validate that the chosen team is in our AP_TOP_25 list
        if picked_team in AP_TOP_25:
            ChampionshipPick.objects.create(
                team_name=picked_team,
                voter=request.user if request.user.is_authenticated else None,
            )
            # Redirect to results after successful vote
            return HttpResponseRedirect(reverse("polls:cfp_results"))

        # If invalid input, redisplay the form with an error
        return render(
            request,
            "polls/cfp_vote.html",
            {
                "teams": AP_TOP_25,
                "error_message": "Please select a valid team.",
            },
        )

    # GET request: show the form
    return render(request, "polls/cfp_vote.html", {"teams": AP_TOP_25})


def cfp_results(request):
    """
    Leaderboard page:
    - Aggregate all ChampionshipPick rows
    - Show vote counts and percentages per team
    """
    # Count how many picks per team, sorted by most-picked
    counts = (
        ChampionshipPick.objects
        .values("team_name")
        .annotate(total=Count("id"))
        .order_by("-total")
    )

    # total votes overall (avoid divide-by-zero)
    grand_total = sum(row["total"] for row in counts) or 1

    # decorate each row with a computed percentage
    results = []
    for row in counts:
        pct = (row["total"] / grand_total) * 100
        results.append({
            "team_name": row["team_name"],
            "votes": row["total"],
            "percent": round(pct, 1),
        })

    return render(
        request,
        "polls/cfp_results.html",
        {
            "results": results,
            "grand_total": grand_total,
        },
    )


# -------------------------
# Original Polls tutorial views
# -------------------------

class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """
        Return the last five published questions (not including future polls).
        """
        return (
            Question.objects.filter(pub_date__lte=timezone.now())
            .order_by("-pub_date")[:5]
        )


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        """
        Exclude any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
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
        # Redisplay the question voting form with an error.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = selected_choice.votes + 1
        selected_choice.save()
        return HttpResponseRedirect(
            reverse("polls:results", args=(question.id,))
        )
