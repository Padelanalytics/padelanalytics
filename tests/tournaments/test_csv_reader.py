from django.test import TestCase

from tournaments.csvReader import CsvReader
from tournaments.models import GameRound, PadelResult, Team


class DjangoCsvFetcherTestCase(TestCase):

    def setUp(self):
        GameRound.objects.create(category="Gold", round="PoolA", number_teams=4)
        GameRound.objects.create(category="Gold", round="PoolA", number_teams=3)
        GameRound.objects.create(category="Gold", round="PoolB", number_teams=3)
        GameRound.objects.create(category="Gold", round="PoolC", number_teams=3)
        GameRound.objects.create(category="Gold", round="PoolD", number_teams=3)
        GameRound.objects.create(category="Gold", round="KO4", number_teams=2)
        GameRound.objects.create(category="Gold", round="KO2", number_teams=2)
        GameRound.objects.create(category="Gold", round="KO1", number_teams=2)
        GameRound.objects.create(category="Gold", round="POS3", number_teams=2)
        GameRound.objects.create(category="Gold", round="PoolA", number_teams=6)


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

    def test_create_padel_tournament_from_csv(self):
        csv_tournament = [
            "Wormser Open 2018;GPS-1000;MO;02.09.2018;;;PoolA;Gold;3;Eckert;Marvin;Strauss;Oliver;Kugele;Nikolai;Thurow;Oliver;2;6;0;6;1;;",
            "Wormser Open 2018;GPS-1000;MO;02.09.2018;;;PoolA;Gold;3;Eckert;Marvin;Strauss;Oliver;Zeller;Fabricio;Matteo;Consonni;2;6;1;6;0;;",
            "Wormser Open 2018;GPS-1000;MO;02.09.2018;;;PoolA;Gold;3;Kugele;Nikolai;Thurow;Oliver;Zeller;Fabricio;Matteo;Consonni;2;1;6;6;3;10;7",
            "Wormser Open 2018;GPS-1000;MO;02.09.2018;;;PoolB;Gold;3;Eckert;Günter;Rupp;Matthias;Heinemann;Nicolas;Kohler;Sebastian;2;6;2;1;6;2;10",
            "Wormser Open 2018;GPS-1000;MO;02.09.2018;;;PoolB;Gold;3;Eckert;Günter;Rupp;Matthias;Petzold;Uwe;Lüers;Steffen;2;4;6;1;6;;",
            "Wormser Open 2018;GPS-1000;MO;02.09.2018;;;PoolB;Gold;3;Heinemann;Nicolas;Kohler;Sebastian;Petzold;Uwe;Lüers;Steffen;2;4;6;5;7;;",
            "Wormser Open 2018;GPS-1000;MO;02.09.2018;;;PoolC;Gold;3;Gutiérrez Soria;Ignacio;Thavisin;Ben;Hahn;Heiko;Jordan;Tobias;2;6;0;6;3;;",
            "Wormser Open 2018;GPS-1000;MO;02.09.2018;;;PoolC;Gold;3;Gutiérrez Soria;Ignacio;Thavisin;Ben;Dreilich;Peter;Fernández Cruz;José Carlos;2;6;0;6;0;;",
            "Wormser Open 2018;GPS-1000;MO;02.09.2018;;;PoolC;Gold;3;Hahn;Heiko;Jordan;Tobias;Dreilich;Peter;Fernández Cruz;José Carlos;2;6;1;6;2;;",
            "Wormser Open 2018;GPS-1000;MO;02.09.2018;;;PoolD;Gold;3;von Ketelhodt;Michael;Petzold;Thomas;Dreissigacker;Wolf;Kaiser;Sascha;2;6;0;6;0;;",
            "Wormser Open 2018;GPS-1000;MO;02.09.2018;;;PoolD;Gold;3;von Ketelhodt;Michael;Petzold;Thomas;Niekisch;Dirk;Bäcker;Katrin;2;6;0;6;0;;",
            "Wormser Open 2018;GPS-1000;MO;02.09.2018;;;PoolD;Gold;3;Dreissigacker;Wolf;Kaiser;Sascha;Niekisch;Dirk;Bäcker;Katrin;2;6;1;5;7;10;4",
            "Wormser Open 2018;GPS-1000;MO;02.09.2018;;;KO4;Gold;2;Eckert;Marvin;Strauss;Oliver;Heinemann;Nicolas;Kohler;Sebastian;2;6;0;6;2;;",
            "Wormser Open 2018;GPS-1000;MO;02.09.2018;;;KO4;Gold;2;Gutiérrez Soria;Ignacio;Thavisin;Ben;Dreissigacker;Wolf;Kaiser;Sascha;2;6;0;6;0;;",
            "Wormser Open 2018;GPS-1000;MO;02.09.2018;;;KO4;Gold;2;Kugele;Nikolai;Thurow;Oliver;Petzold;Uwe;Lüers;Steffen;2;2;6;4;6;;",
            "Wormser Open 2018;GPS-1000;MO;02.09.2018;;;KO4;Gold;2;Hahn;Heiko;Jordan;Tobias;von Ketelhodt;Michael;Petzold;Thomas;2;3;6;1;6;;",
            "Wormser Open 2018;GPS-1000;MO;02.09.2018;;;KO2;Gold;2;Eckert;Marvin;Strauss;Oliver;Gutiérrez Soria;Ignacio;Thavisin;Ben;2;4;6;1;6;;",
            "Wormser Open 2018;GPS-1000;MO;02.09.2018;;;KO2;Gold;2;Petzold;Uwe;Lüers;Steffen;von Ketelhodt;Michael;Petzold;Thomas;2;2;6;0;6;;",
            "Wormser Open 2018;GPS-1000;MO;02.09.2018;;;KO1;Gold;2;Gutiérrez Soria;Ignacio;Thavisin;Ben;von Ketelhodt;Michael;Petzold;Thomas;2;6;4;6;4;;",
            "Wormser Open 2018;GPS-1000;MO;02.09.2018;;;POS3;Gold;2;Eckert;Marvin;Strauss;Oliver;Petzold;Uwe;Lüers;Steffen;2;6;2;6;0;;",

            "Wormser Open 2019;GPS-250;MO;10.08.2019;;;PoolA;Gold;6;Bott;Frederick;Thavisin;Ben;Saugy;Mael;Dietz;Timo;2;9;8;;;;",
            "Wormser Open 2019;GPS-250;MO;10.08.2019;;;PoolA;Gold;6;Müller;Hans Ole;Gutiérrez Soria;Ignacio;von Ketelhodt;Michael;Petzold;Uwe;2;9;4;;;;",
            "Wormser Open 2019;GPS-250;MO;10.08.2019;;;PoolA;Gold;6;Seitz;Markus;Platt;Markus;Petzold;Thomas;Kugele;Nikolai;2;1;9;;;;",
            "Wormser Open 2019;GPS-250;MO;10.08.2019;;;PoolA;Gold;6;Bott;Frederick;Thavisin;Ben;Müller;Hans Ole;Gutiérrez Soria;Ignacio;2;9;6;;;;",
            "Wormser Open 2019;GPS-250;MO;10.08.2019;;;PoolA;Gold;6;Seitz;Markus;Platt;Markus;von Ketelhodt;Michael;Petzold;Uwe;2;2;9;;;;",
            "Wormser Open 2019;GPS-250;MO;10.08.2019;;;PoolA;Gold;6;Saugy;Mael;Dietz;Timo;Petzold;Thomas;Kugele;Nikolai;2;9;6;;;;",
            "Wormser Open 2019;GPS-250;MO;10.08.2019;;;PoolA;Gold;6;Bott;Frederick;Thavisin;Ben;Seitz;Markus;Platt;Markus;2;9;1;;;;",
            "Wormser Open 2019;GPS-250;MO;10.08.2019;;;PoolA;Gold;6;Saugy;Mael;Dietz;Timo;Müller;Hans Ole;Gutiérrez Soria;Ignacio;2;5;9;;;;",
            "Wormser Open 2019;GPS-250;MO;10.08.2019;;;PoolA;Gold;6;von Ketelhodt;Michael;Petzold;Uwe;Petzold;Thomas;Kugele;Nikolai;2;9;6;;;;",
            "Wormser Open 2019;GPS-250;MO;10.08.2019;;;PoolA;Gold;6;Saugy;Mael;Dietz;Timo;Seitz;Markus;Platt;Markus;2;9;1;;;;",
            "Wormser Open 2019;GPS-250;MO;10.08.2019;;;PoolA;Gold;6;Bott;Frederick;Thavisin;Ben;von Ketelhodt;Michael;Petzold;Uwe;2;9;3;;;;",
            "Wormser Open 2019;GPS-250;MO;10.08.2019;;;PoolA;Gold;6;Müller;Hans Ole;Gutiérrez Soria;Ignacio;Petzold;Thomas;Kugele;Nikolai;2;9;2;;;;",
            "Wormser Open 2019;GPS-250;MO;10.08.2019;;;PoolA;Gold;6;Saugy;Mael;Dietz;Timo;von Ketelhodt;Michael;Petzold;Uwe;2;9;6;;;;",
            "Wormser Open 2019;GPS-250;MO;10.08.2019;;;PoolA;Gold;6;Bott;Frederick;Thavisin;Ben;Petzold;Thomas;Kugele;Nikolai;2;9;5;;;;",
            "Wormser Open 2019;GPS-250;MO;10.08.2019;;;PoolA;Gold;6;Müller;Hans Ole;Gutiérrez Soria;Ignacio;Seitz;Markus;Platt;Markus;2;9;0;;;;"
        ]

        # create all the games of the tournament
        for csv_game in csv_tournament:
            csv_reader = CsvReader(CsvReader.PADEL_GAME)
            game = csv_reader.get_csv_object(csv_game.split(";"))
            csv_reader.create_django_object(game)
        # test number of teams and number of team members
        teams = Team.objects.all()
        # self.assertEqual(len(teams), 18) # 12 (2018)+6(2019)
        for team in teams:
            players = team.players.all()
            for player in players:
                print(player)
            self.assertEqual(len(players), 2)
            print("------------------------------------------------- End of team")