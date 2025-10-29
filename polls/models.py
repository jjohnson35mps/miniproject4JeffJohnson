### INF601 - Advanced Programming in Python
### Jeff Johnson
### Mini Project 4

import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User  # new import so we can associate a vote with a user


class Question(models.Model):
    question_text = models.CharField("question text", max_length=200)
    pub_date = models.DateTimeField("date published")

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        """
        Returns True if the question was published within the last day.
        Used in admin list display.
        """
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    was_published_recently.admin_order_field = "pub_date"
    was_published_recently.boolean = True
    was_published_recently.short_description = "Published recently?"


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField("choice text", max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


class ChampionshipPick(models.Model):
    """
    Stores a single vote for who will win the 2025 College Football Playoff.
    Each row is one user's pick.
    """
    team_name = models.CharField(max_length=100)
    voted_at = models.DateTimeField(auto_now_add=True)
    voter = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="If the user was logged in when they voted."
    )

    def __str__(self):
        return f"{self.team_name} @ {self.voted_at}"
