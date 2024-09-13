from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from django.forms.models import model_to_dict
from teams.models import Team

from utils import data_processing
from exceptions import (
    NegativeTitlesError,
    InvalidYearCupError,
    ImpossibleTitlesError,
)


class TeamView(APIView):
    def post(self, request: Request) -> Response:
        try:
            data_processing(request.data)
            TEAM = Team.objects.create(**request.data)
        except (
            ImpossibleTitlesError,
            InvalidYearCupError,
            NegativeTitlesError,
        ) as e:
            return Response(
                {"error": e.message},
                status=400,
            )

        except Exception as e:
            return Response({"error": str(e)}, status=500)

        return Response(model_to_dict(TEAM), status=201)

    def get(self, request: Request) -> Response:
        teams = Team.objects.all()
        return Response([model_to_dict(team) for team in teams])


class OneTeamView(APIView):
    def get(self, request: Request, team_id) -> Response:
        try:
            team = Team.objects.get(pk=team_id)
        except (Team.DoesNotExist, ValueError):
            return Response({"message": "Team not found"}, status=404)

        return Response(model_to_dict(team))

    def patch(self, request: Request, team_id) -> Response:
        try:
            TO_UPDATE = Team.objects.get(pk=team_id)
            UPDATED_TEAM = {**model_to_dict(TO_UPDATE), **request.data}
            data_processing(UPDATED_TEAM)
            TEAM = Team(**UPDATED_TEAM)
            TEAM.id = team_id
            TEAM.save()

        except (Team.DoesNotExist, ValueError):
            return Response({"message": "Team not found"}, status=404)

        except (
            ImpossibleTitlesError,
            InvalidYearCupError,
            NegativeTitlesError,
        ) as e:
            return Response(
                {"error": e.message},
                status=400,
            )

        return Response(UPDATED_TEAM)

    def delete(self, request: Request, team_id) -> Response:
        try:
            Team.objects.get(pk=team_id).delete()
        except (Team.DoesNotExist, ValueError):
            return Response({"message": "Team not found"}, status=404)

        return Response(status=204)
