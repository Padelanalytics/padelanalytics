# Coppyright (c) 2015 Francisco Javier Revilla Linares to present.
# All rights reserved.
import unittest
from datetime import date

from django.test import TestCase

from tournaments.helpers import compute_ranking_positions
from tournaments.models import PadelRanking, Person


class ServiceTestCase(TestCase):
    @unittest.skip("skip the test. Feature is not complete.")
    def test_compute_ranking_positions(self):
        a = Person.objects.create(first_name="A", last_name="A")
        b = Person.objects.create(first_name="B", last_name="B")
        c = Person.objects.create(first_name="C", last_name="C")
        d = Person.objects.create(first_name="D", last_name="D")
        e = Person.objects.create(first_name="E", last_name="E")
        f = Person.objects.create(first_name="F", last_name="F")

        PadelRanking.objects.create(
            division="MO",
            country="GERMANY",
            date=date(2020, 1, 1),
            points=1000,
            person_id=a.id,
        )
        PadelRanking.objects.create(
            division="MO",
            country="GERMANY",
            date=date(2020, 1, 1),
            points=1000,
            person_id=b.id,
        )
        PadelRanking.objects.create(
            division="MO",
            country="GERMANY",
            date=date(2020, 1, 1),
            points=2000,
            person_id=c.id,
        )
        PadelRanking.objects.create(
            division="MO",
            country="GERMANY",
            date=date(2020, 1, 1),
            points=2000,
            person_id=d.id,
        )
        PadelRanking.objects.create(
            division="MO",
            country="GERMANY",
            date=date(2020, 1, 1),
            points=1000,
            person_id=e.id,
        )
        PadelRanking.objects.create(
            division="MO",
            country="GERMANY",
            date=date(2020, 1, 1),
            points=500,
            person_id=f.id,
        )

        compute_ranking_positions()

        ranking = PadelRanking.objects.all().order_by(
            "-country", "-division", "-date", "-points"
        )

        for i in range(len(ranking)):
            rk = ranking[i]
            print(rk.position)
            if i in [0, 1]:
                self.assertEqual(rk.position, 1)
            elif i in [2, 4]:
                self.assertEqual(rk.position, 2)
            elif i == 5:
                self.assertEqual(rk.position, 3)
