from django.test import TestCase

from tournaments.models import PadelResult


class PadelResultTestCase(TestCase):
    def test_game_winner(self):
        scores = [5, 7, 6, 3, 11, 9]
        result = PadelResult.create(scores)
        self.assertEqual(result.winner, 1)
