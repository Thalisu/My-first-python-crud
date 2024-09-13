from django.urls import path
from teams.views import TeamView, OneTeamView

urlpatterns = [
    path("teams/", TeamView.as_view()),
    path("teams/<int:team_id>/", OneTeamView.as_view()),
]
