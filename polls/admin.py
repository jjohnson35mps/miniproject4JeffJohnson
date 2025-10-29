### INF601 - Advanced Programming in Python
### Jeff Johnson
### Mini Project 4

from django.contrib import admin
from .models import Question, Choice, ChampionshipPick


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3  # show 3 empty Choice slots by default


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {"fields": ["question_text"]}),
        ("Date information", {"fields": ["pub_date"], "classes": ["collapse"]}),
    ]
    inlines = [ChoiceInline]
    list_display = ("question_text", "pub_date", "was_published_recently")
    list_filter = ["pub_date"]
    search_fields = ["question_text"]


@admin.register(ChampionshipPick)
class ChampionshipPickAdmin(admin.ModelAdmin):
    list_display = ("team_name", "voted_at", "voter")
    list_filter = ("team_name", "voted_at")
    search_fields = ("team_name", "voter__username")


admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
