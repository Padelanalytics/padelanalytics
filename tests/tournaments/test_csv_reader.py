from django.test import TestCase

from tournaments.csvReader import CsvReader
from tournaments.models import PadelResult, GameRound


class DjangoCsvFetcherTestCase(TestCase):
    def setUp(self):
        GameRound.objects.create(category="Gold", round="PoolA", number_teams=4)

    def test_create_padel_game_from_csv(self):
        csv_line = (
            "Cuxhavener Lokales Turnier 2019;GPS-100;MO;20.04.2019;;;PoolA;Gold;4;Glüsing;Arne;Hagen;Ralf;Brokoriow;"
            "Danny;Couto;Jaime;2;5;7;6;3;11;9"
        ).split(";")
        csv_reader = CsvReader(CsvReader.PADEL_GAME)
        padel_result = csv_reader.get_csv_object(csv_line)
        csv_reader.create_django_object(padel_result)
        padel_result = PadelResult.objects.first()
        self.assertEqual(padel_result.winner, 1)
