from rest_framework import viewsets
from rest_framework import generics

from rest_framework.exceptions import APIException
from tournaments.serializers import PadelRankingSerializer


class APIValueError(APIException):
    status_code = 400
    default_detail = 'Request with wrong parameters, fix it and try again.'
    default_code = 'wrong parameters'


class PadelRankingList(generics.ListAPIView):
    # example:
    # http://127.0.0.1:8000/api/ranking?federation=WPT&division=MO&date=2020-03-02
    
    serializer_class = PadelRankingSerializer

    def get_queryset(self):
        from tournaments.models import PadelRanking

        federation = self.request.query_params.get('federation', None)
        date = self.request.query_params.get('date', None)
        division = self.request.query_params.get('division', None)

        if federation is None or date is None or division is None:
            raise APIValueError()

        return PadelRanking.objects.filter(
            country=federation,
            date=date,
            division=division
            ).order_by('position')