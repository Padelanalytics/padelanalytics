from rest_framework import serializers

from tournaments.models import PadelRanking, Person


class PersonSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Person
        fields = ["first_name", "last_name"]


class PadelRankingSerializer(serializers.HyperlinkedModelSerializer):
    person = PersonSerializer()

    class Meta:
        model = PadelRanking
        fields = ["date", "position", "points", "person"]
