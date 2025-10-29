# ### INF601 - Advanced Programming in Python
# ### Jeff Johnson
# ### Mini Project 4

from django.contrib import admin
from .models import Question, Choice, ChampionshipPick


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("question_text", "pub_date", "was_published_recently")
    list_filter = ("pub_date",)
    search_fields = ("question_text",)
    date_hierarchy = "pub_date"
    inlines = [ChoiceInline]


@admin.register(ChampionshipPick)
class ChampionshipPickAdmin(admin.ModelAdmin):
    list_display = ("team_name", "voter", "voted_at")          # matches model
    list_filter  = ("team_name", "voter", "voted_at")          # matches model
    search_fields = ("team_name", "voter__username", "voter__email")
    ordering = ("-voted_at",)
