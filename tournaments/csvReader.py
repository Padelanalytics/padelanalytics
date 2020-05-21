""" Collection of classes and methods to import csv data

This scripts offers methods to the user to read csv files and import the readed data into the
database. The idea is to have all the statidistical data in csv files (tournaments, players,
rankings) and extend this files with new information (new tournament or ranking) or fix any
mistake on the information on the files (e.g. wrong player name or game result) and afterwards
delete all the stadistical data from the database and import it from zero again.

Usually when a complex csv object is imported the following rutine is followed:

Lets say the object is a Game, a Game contains two teams, each team contains 2 or more players a
player contains a person.

1) We search for a person, if it does not exists a new person is created otherwise we used the
found person.

2) Search for a team with the found persons, if it not exists create a new team with the found
persons as a players

3) Search for the tournament of the game, if does not exits create it.

4) Finally create the game.
"""


import csv
import logging

import itertools

from tournaments import games
from tournaments import csvdata
from tournaments.models import Club
from tournaments.models import Game
from tournaments.models import GameField
from tournaments.models import GameRound
from tournaments.models import PadelRanking
from tournaments.models import PadelResult
from tournaments.models import Person
from tournaments.models import Player
from tournaments.models import PlayerStadistic
from tournaments.models import Team
from tournaments.models import Tournament
from tournaments.models import get_player_gender
from tournaments.service import all_mondays_from


from django.core.exceptions import MultipleObjectsReturned
from django.core.exceptions import ObjectDoesNotExist

# Get an instance of a logger
logger = logging.getLogger(__name__)


class DjangoSimpleFetcher:
    @staticmethod
    def print_fetch_result(obj, created=False):
        if created:
            print('Created {:s}: '.format(type(obj).__name__) + str(obj))
            logger.debug('Created {:s}: '.format(type(obj).__name__) + str(obj))

        else:
            if obj is None:
                print('Neither object found or created.\n')
                logger.debug('Neither object found or created.\n')
            else:
                print('Found {:s}: '.format(type(obj).__name__) + str(obj))
                logger.debug('Found {:s}: '.format(type(obj).__name__) + str(obj))

    @staticmethod
    def get_or_create_tournament(federation, tournament_name, tournament_division, type, ranking=None, date=None):
        result = Tournament.objects.get_or_create(
            federation=federation,
            name=tournament_name,
            division=tournament_division,
            type=type,
            padel_serie=ranking,
            date=date)
        return result

    @staticmethod
    def get_team(team_name, division):
        return Team.objects.get(name=team_name, division=division)

    @staticmethod
    def get_or_create_team(team_name, team_division):
        result = Team.objects.get_or_create(name=team_name, division=team_division)
        return result

    @staticmethod
    def get_or_create_person(first_name, last_name, gender=Person.UNKNOWN, nationality=None, born=None):
        try:
            result = Person.objects.get(first_name=first_name, last_name=last_name)
            update = False
            if gender != Person.UNKNOWN and result.gender == Person.UNKNOWN:
                result.gender = gender
                result.save()
                #Person.objects.get(first_name=first_name, last_name=last_name).update(gender=gender)
                update = True
            if nationality and result.nationality is None:
                result.nationality = nationality
                Person.objects.get(first_name=first_name, last_name=last_name).update(nationality=nationality)
                update = True
            if born and result.born is None:
                result.born = born
                Person.objects.get(first_name=first_name, last_name=last_name).update(born=born)
                update = True
            result = result, update
        except MultipleObjectsReturned:
            result = Person.objects.get(first_name=first_name, last_name=last_name, gender=gender)
            result = result, False
        except ObjectDoesNotExist:
            result = Person.objects.get_or_create(first_name=first_name, last_name=last_name, gender=gender)
        return result

    @staticmethod
    def get_or_create_player(person, team, number, tournament_id=None):
        number2 = None
        if number:
            try:
                number2 = int(number)
            except ValueError:
                pass
        obj, created = Player.objects.get_or_create(person=person, team=team, number=number2)
        if tournament_id is None:
            pass
        else:
            obj.tournaments_played.add(tournament_id)
        return obj, created

    @staticmethod
    def get_game(tournament, phase, local, local_score, visitor, visitor_score, strict=True):
        try:
            # first try with given local and visitor teams and scores:
            game = Game.objects.get(
                    tournament=tournament,
                    local=local,
                    visitor=visitor,
                    local_score=local_score,
                    visitor_score=visitor_score,
                    phase=phase)
            return game
        except Game.DoesNotExist as ex:
            if strict:
                raise ex
        # else: ignore exception and go for a second try changing local and visitor teams and scores:
        game = Game.objects.get(
                tournament=tournament,
                visitor=local,
                local=visitor,
                visitor_score=local_score,
                local_score=visitor_score,
                phase=phase)
        return game

    @staticmethod
    def create_game(tournament, phase, field, time, local_team, visitor_team, local_score, visitor_score, padel_scores):
        if padel_scores:
            result_padel = PadelResult.create(padel_scores.scores)
            result_padel.save()
        else:
            result_padel = None

        result = Game.objects.get_or_create(
                tournament=tournament,
                local=local_team,
                visitor=visitor_team,
                local_score=local_score,
                visitor_score=visitor_score,
                phase=phase,
                field=field,
                time=time,
                result_padel=result_padel)

        return result

    @staticmethod
    def get_or_create_game_phase(category, round, number, create):
        get_round = round
        print(get_round.encode('utf-8'))
        if get_round.encode('utf-8') == b'\xc2\xbc' or get_round.encode(
                'utf-8') == b'\xc2\xbd' or get_round == '\xc2\xbc':
            get_round = '1/4'
        if create:
            result = GameRound.objects.get_or_create(category=category, round=get_round, number_teams=number)
        else:
            result = GameRound.objects.get(category=category, round=get_round, number_teams=number), False
        return result

    @staticmethod
    def get_or_create_nts_statistic(game, player, scores, mvp=None):
        if scores and int(scores) > 0:
            #result = PlayerStadistic.objects.get_or_create(game=game, player=player, points=scores)
            try:
                player = PlayerStadistic.objects.get(game=game, player=player)
                player.points = scores
                player.mvp = mvp
                player.save()
                return player, True
            except PlayerStadistic.DoesNotExist:
                result = PlayerStadistic.objects.get_or_create(game=game, player=player, points=scores)
            return result
        else:
            return None, False

    @staticmethod
    def get_or_create_fit_statistic(tournament, player, played, scores, mvp):
        try:
            player = PlayerStadistic.objects.get(tournament=tournament, player=player)
            player.played = played
            player.points = scores
            player.mvp = mvp
            player.save()
            return player, True
        except PlayerStadistic.DoesNotExist:
            result = PlayerStadistic.objects.get_or_create(
                tournament=tournament, player=player, played=played, points=scores, mvp=mvp)
        return result

    @staticmethod
    def get_or_create_padel_ranking(ranking, monday, person):
        try:
            obj = PadelRanking.objects.get(country=ranking.country, date=monday, circuit=ranking.circuit,
                                           division=ranking.division, person=person.id)
            obj.points = ranking.points
            obj.plus = ranking.plus
            obj.minus = ranking.minus
            obj.save(force_update=True)
        except PadelRanking.DoesNotExist:
            obj = PadelRanking.objects.create(
                country=ranking.country, date=monday, circuit=ranking.circuit, division=ranking.division, person=person,
                points=ranking.points, plus=ranking.plus, minus=ranking.minus)
        return obj

    @staticmethod
    def create_padel_ranking(ranking):
        from datetime import datetime
        #date_format = "%Y-%m-%d"
        date_format = "%d.%m.%Y"
        #date_format = "%d/%m/%Y"
        person, b = DjangoCsvFetcher.create_padel_person(ranking)
        mondays = all_mondays_from(datetime.strptime(ranking.date, date_format))
        for monday in mondays:
            obj = DjangoSimpleFetcher.get_or_create_padel_ranking(ranking, monday, person)
        return obj, True

    @staticmethod
    def assign_club_to_person(person_club):
        person = Person.objects.get(
            first_name=person_club.first_name,
            last_name=person_club.last_name)

        if person_club.club_name:
            club = Club.objects.get(name=person_club.club_name)
            person.club = club
        if person_club.country:
            person.country = person_club.country

        person.save()


def add_team_to_tournament(tournament, team):
    if not tournament.teams.filter(id=team.id).exists():
        tournament.teams.add(team)
        tournament.save()
        print("Added team %s into tournament %s" % (team.name, tournament.name))
    else:
        print("Tournament %s already has the team %s" % (tournament.name, team.name))


def create_or_fetch_team(pName, pDivision, type=None):
    if type == 'PADEL':
        assert len(pName) == 2, "pName must be a list with two strings"
        name = pName[0] + " - " + pName[1]
    else:
        name = pName

    result = Team.objects.get_or_create(
            name=name,
            division=pDivision,
    )
    return result


def check_team_players(team, person1, person2):
    if not team.pair:
        raise ValueError("This method only makes sense if the team is a pair.")
    players = list(team.players.all())
    if players[0].first_name in ['Bye', 'bye'] or players[1].first_name in ['Bye', 'bye']:
        return True
    if len(players) != 2:
        raise ValueError("Team object has an invalid number of players.")
    if (players[0].pk == person1.pk or players[0].pk == person2.pk) and (
        players[1].pk == person1.pk or players[1].pk == person2.pk):
        return True
    return False


def create_or_fetch_team2(person1, person2, team_name, team_division, is_pair):
    try:
        team = Team.objects.get(name=team_name)
    except ObjectDoesNotExist:
        # if not exists create one and return it
        return Team.objects.get_or_create(name=team_name)
    except MultipleObjectsReturned:
        # clubs or national teams must be unique
        if not is_pair:
            raise ValueError("Club or national teams must be unique: " + team_name)
        # if there is more than one, find out which one is the right and
        # return it, otherwise create a new team
        teams = Team.objects.filter(name=team_name)
        for t in teams:
            result = check_team_players(t, person1, person2)
            if result:
                return t, False
        return Team.objects.create(name=team_name), True

    if is_pair and not check_team_players(team, person1, person2):
        return Team.objects.create(name=team_name), True
    else:
        return team, False


def printCF(obj, created):
    if obj:
        if created:
            print('Created {:s}:\n {:s}'.format(obj.__class__.__name__, obj))
        else:
            print('Found {:s}:\n {:s}'.format(obj.__class__.__name__, obj))
    else:
        print('ERROR\n')


class DjangoCsvFetcher:

    @staticmethod
    def create_csv_phase(csv_game, create):
        if not isinstance(csv_game, csvdata.CsvGame) and not isinstance(csv_game, games.Game):
            assert 0, "Wrong game to read: " + csv_game

        round = csv_game.round
        if round.encode('utf-8') == b'\xc2\xbc':
            round = '1/4'
        print(round.encode('utf-8'))

        if create:
            result, created = GameRound.objects.get_or_create(
                    category=csv_game.category,
                    round=round,
                    number_teams=csv_game.nteams)
        else:
            result, created = GameRound.objects.get(
                    category=csv_game.category,
                    round=round,
                    number_teams=csv_game.nteams), False

        DjangoSimpleFetcher.print_fetch_result(result, created)
        return result, created


    @staticmethod
    def create_club(csv_club):
        try:
            result = Club.objects.get(federation=csv_club.federation, name=csv_club.name)
            created = False
            result.city = csv_club.city
            result.province = csv_club.province
            result.postcode = csv_club.postcode
            result.email = csv_club.email
            result.phone = csv_club.phone
            result.address = csv_club.address
            result.indoor_courts = csv_club.indoor_courts
            result.outdoor_courts = csv_club.outdoor_courts
            result.website = csv_club.website
            result.save()

        except ObjectDoesNotExist:
            created = True
            result = Club.objects.create(
                federation=csv_club.federation,
                name=csv_club.name,
                city=csv_club.city,
                province=csv_club.province,
                postcode=csv_club.postcode,
                email=csv_club.email,
                phone=csv_club.phone,
                address=csv_club.address,
                indoor_courts=csv_club.indoor_courts,
                outdoor_courts=csv_club.outdoor_courts,
                website=csv_club.website)

        DjangoSimpleFetcher.print_fetch_result(result, created)
        return result, created


    def create_padel_person(ranking):
        gender = get_player_gender(ranking.division)
        person = DjangoSimpleFetcher.get_or_create_person(
            first_name=ranking.first_name, last_name=ranking.last_name, gender=gender)
        return person

    def create_padel_persons(game):
        if game.padel_team_names:
            gender = get_player_gender(game.division)
            # local team first pair
            person1, created = DjangoSimpleFetcher.get_or_create_person(
                    game.padel_team_names.local_first_first_name,
                    game.padel_team_names.local_first_last_name,
                    gender)
            DjangoSimpleFetcher.print_fetch_result(person1, created)
            # local team second pair
            person2, created = DjangoSimpleFetcher.get_or_create_person(
                    game.padel_team_names.local_second_first_name,
                    game.padel_team_names.local_second_last_name,
                    gender)
            DjangoSimpleFetcher.print_fetch_result(person2, created)
            # visitor team first pair
            person3, created = DjangoSimpleFetcher.get_or_create_person(
                    game.padel_team_names.visitor_first_first_name,
                    game.padel_team_names.visitor_first_last_name,
                    gender)
            DjangoSimpleFetcher.print_fetch_result(person3, created)
            # visitor team second pair
            person4, created = DjangoSimpleFetcher.get_or_create_person(
                    game.padel_team_names.visitor_second_first_name,
                    game.padel_team_names.visitor_second_last_name,
                    gender)
            DjangoSimpleFetcher.print_fetch_result(person4, created)
            return (person1, person2, person3, person4)

    @staticmethod
    def create_padel_csv_game(game):
        type = "PADEL"

        print(game.date_time, game)

        # create tournament
        tournament, created = DjangoSimpleFetcher.get_or_create_tournament(
            game.federation,
            game.tournament_name,
            game.division,
            type,
            game.ranking,
            game.date_time)

        # create phase
        phase, created = DjangoCsvFetcher.create_csv_phase(game, False)
        try:
            time = game.time
        except AttributeError:
            time = None

        if game.field:
            field, created = GameField.objects.get_or_create(name=game.field)
        else:
            field = None

        # create persons
        persons = DjangoCsvFetcher.create_padel_persons(game)

        # create local team
        local_team, created = create_or_fetch_team2(persons[0], persons[1], game.local, game.division, game.is_pair)
        DjangoSimpleFetcher.print_fetch_result(local_team, created)
        add_team_to_tournament(tournament, local_team)

        # create local players
        DjangoSimpleFetcher.get_or_create_player(persons[0], local_team, None, tournament.id)
        DjangoSimpleFetcher.get_or_create_player(persons[1], local_team, None, tournament.id)

        # create visitor team
        visitor_team, created = create_or_fetch_team2(persons[2], persons[3], game.visitor, game.division, game.is_pair)
        DjangoSimpleFetcher.print_fetch_result(visitor_team, created)
        add_team_to_tournament(tournament, visitor_team)

        # create visitor players
        DjangoSimpleFetcher.get_or_create_player(persons[2], visitor_team, None, tournament.id)
        DjangoSimpleFetcher.get_or_create_player(persons[3], visitor_team, None, tournament.id)

        # create game
        game, created = DjangoSimpleFetcher.create_game(
                tournament, phase, field, time, local_team, visitor_team,
                game.local_score, game.visitor_score, game.padel_result)

    @staticmethod
    def create_touch_csv_game(game):
        # if not isinstance(game, csvdata.CsvGame):
        #    assert 0, "Wrong game to read: " + game
        type = "TOUCH"
        padel_result = None

        tournament, created = DjangoSimpleFetcher.get_or_create_tournament(game.federation, game.tournament_name, game.division, type)
        DjangoSimpleFetcher.print_fetch_result(tournament, created)

        local_team, created = create_or_fetch_team(game.local, game.division)
        DjangoSimpleFetcher.print_fetch_result(local_team, created)

        add_team_to_tournament(tournament, local_team)
        # if created:
        #    add_team_to_tournament(tournament, local_team)
        phase, created = DjangoCsvFetcher.create_csv_phase(game, False)
        try:
            time = game.time
        except AttributeError:
            time = None

        if game.field:
            field, created = GameField.objects.get_or_create(name=game.field)
            DjangoSimpleFetcher.print_fetch_result(field, created)
        else:
            field = None

        visitor_team, created = create_or_fetch_team(game.visitor, game.division)
        DjangoSimpleFetcher.print_fetch_result(visitor_team, created)

        add_team_to_tournament(tournament, visitor_team)
        # if created:
        #    add_team_to_tournament(tournament, visitor_team)
        game, created = DjangoSimpleFetcher.create_game(
                tournament, phase, field, time, local_team, visitor_team,
                game.local_score, game.visitor_score, padel_result)
        DjangoSimpleFetcher.print_fetch_result(game, created)
        # assert created, "The game already exists"

    @staticmethod
    def create_csv_fit_statistic(csv_stats):
        if not isinstance(csv_stats, csvdata.FitStatistic):
            assert 0, "Wrong statistic to read: " + csv_stats

        tournament, created = DjangoSimpleFetcher.get_or_create_tournament(
                "",
                csv_stats.tournament_name,
                csv_stats.division,
                "TOUCH")
        DjangoSimpleFetcher.print_fetch_result(tournament, created)

        team, created = DjangoSimpleFetcher.get_or_create_team(csv_stats.team, csv_stats.division)
        DjangoSimpleFetcher.print_fetch_result(team, created)

        person, created = DjangoSimpleFetcher.get_or_create_person(
                csv_stats.first_name,
                csv_stats.last_name,
                csv_stats.gender)
        DjangoSimpleFetcher.print_fetch_result(person, created)

        player, created = DjangoSimpleFetcher.get_or_create_player(person, team, csv_stats.number, tournament)
        DjangoSimpleFetcher.print_fetch_result(player, created)

        fit_stat, created = DjangoSimpleFetcher.get_or_create_fit_statistic(
                tournament, player, csv_stats.played, csv_stats.scores, csv_stats.mvp)
        DjangoSimpleFetcher.print_fetch_result(fit_stat, created)

    @staticmethod
    def create_csv_nts_player_statistic(csv_stats):
        if not isinstance(csv_stats, csvdata.CsvNTSStatistic):
            assert 0, "Wrong stadistic to read: " + csv_stats

        tournament, created = DjangoSimpleFetcher.get_or_create_tournament(
                "",
                csv_stats.tournament_name,
                csv_stats.division,
                "TOUCH")
        DjangoSimpleFetcher.print_fetch_result(tournament, created)

        team, created = DjangoSimpleFetcher.get_or_create_team(csv_stats.team, csv_stats.division)
        DjangoSimpleFetcher.print_fetch_result(team, created)

        person, created = DjangoSimpleFetcher.get_or_create_person(
                csv_stats.first_name,
                csv_stats.last_name,
                csv_stats.gender)
        DjangoSimpleFetcher.print_fetch_result(person, created)

        player, created = DjangoSimpleFetcher.get_or_create_player(person, team, csv_stats.number, tournament)
        DjangoSimpleFetcher.print_fetch_result(player, created)

        if csv_stats.visitor_score:  # if true nts stadistic otherwise player insert.
            local_team = DjangoSimpleFetcher.get_team(csv_stats.local, csv_stats.division)
            DjangoSimpleFetcher.print_fetch_result(local_team)

            visitor_team = DjangoSimpleFetcher.get_team(csv_stats.visitor, csv_stats.division)
            DjangoSimpleFetcher.print_fetch_result(visitor_team)

            phase, created = DjangoSimpleFetcher.get_or_create_game_phase(
                    csv_stats.category, csv_stats.round, csv_stats.team_numbers, False)
            DjangoSimpleFetcher.print_fetch_result(phase, created)

            game = DjangoSimpleFetcher.get_game(tournament, phase, local_team, csv_stats.local_score,
                                                visitor_team, csv_stats.visitor_score, False)
            DjangoSimpleFetcher.print_fetch_result(game)

            nts_stat, created = DjangoSimpleFetcher.get_or_create_nts_statistic(
                    game, player, csv_stats.tries)
            DjangoSimpleFetcher.print_fetch_result(nts_stat, created)
        else:
            print('GameStadistic skipped: there are no tries for player: {:s}\n '.format(str(player)))


class CsvReader:
    (PHASE, TOURNAMENT, NTS_STATISTIC, FIT_STATISTIC, PADEL_GAME, PERSON, PADEL_RANKING, PADEL_PLAYER_CLUB, CLUB) = range(9)

    def __init__(self, type):
        if type in [self.PHASE, self.TOURNAMENT, self.NTS_STATISTIC, self.FIT_STATISTIC, self.PADEL_GAME, self.PERSON,
                    self.PADEL_RANKING, self.PADEL_PLAYER_CLUB, self.CLUB]:
            self._fexit = '####'
            self._exit_text = '\n Force exit #### :)\n'
            self._type = type
        else:
            assert 0, "Wrong reader creation: " + type

    @staticmethod
    def print_row_to_read(csv):
        print('\nRow to read:\n' + str(csv) + '\n')

    def print_file_footer(self, arg):
        print('\nFinished reading {:s}...\n'.format(arg))

    def print_fetch_result(self, obj, created):
        if created:
            print('Created {:s}:\n'.format(self._type) + str(obj))
        else:
            print('Found {:s}:\n'.format(self._type) + str(obj))

    def get_csv_object(self, row):
        if self._type == self.PHASE:
            result = csvdata.CsvPhase(row)
        elif self._type == self.TOURNAMENT:
            result = csvdata.CsvGame(row, None, None, None)
        elif self._type == self.NTS_STATISTIC:
            result = csvdata.CsvNTSStatistic(row)
        elif self._type == self.FIT_STATISTIC:
            result = csvdata.FitStatistic.from_array(row)
        elif self._type == self.PADEL_GAME:
            result = games.Game.padel_from_csv_list(row)
        elif self._type == self.PERSON:
            result = csvdata.create_person(row)
        elif self._type == self.PADEL_RANKING:
            result = csvdata.create_padel_ranking(row)
        elif self._type == self.PADEL_PLAYER_CLUB:
            result = csvdata.create_padel_player_club(row)
        elif self._type == self.CLUB:
            result = csvdata.create_csv_club(row)
        else:
            assert 0, "Wrong object to read: " + self._type
        return result

    def create_django_object(self, csv_object):
        if self._type == self.PHASE and isinstance(csv_object, csvdata.CsvPhase):
            phase, created = DjangoSimpleFetcher.get_or_create_game_phase(
                    csv_object.category, csv_object.round, csv_object.teams, True)
            DjangoSimpleFetcher.print_fetch_result(phase, created)
        elif self._type == self.TOURNAMENT and isinstance(csv_object, csvdata.CsvGame):
            DjangoCsvFetcher.create_touch_csv_game(csv_object)
        elif self._type == self.NTS_STATISTIC and isinstance(csv_object, csvdata.CsvNTSStatistic):
            DjangoCsvFetcher.create_csv_nts_player_statistic(csv_object)
        elif self._type == self.FIT_STATISTIC and isinstance(csv_object, csvdata.FitStatistic):
            DjangoCsvFetcher.create_csv_fit_statistic(csv_object)
        elif self._type == self.PADEL_GAME and isinstance(csv_object, games.Game):
            DjangoCsvFetcher.create_padel_csv_game(csv_object)
        elif self._type == self.PERSON and isinstance(csv_object, Person):
            DjangoSimpleFetcher.get_or_create_person(
                csv_object.first_name, csv_object.last_name, csv_object.gender, csv_object.nationality, csv_object.born)
        elif self._type == self.PADEL_RANKING and isinstance(csv_object, csvdata.Ranking):
            DjangoSimpleFetcher.create_padel_ranking(csv_object)
        elif self._type == self.PADEL_PLAYER_CLUB and isinstance(csv_object, csvdata.PlayerClub):
            DjangoSimpleFetcher.assign_club_to_person(csv_object)
        elif self._type == self.CLUB and isinstance(csv_object, csvdata.CsvClub):
            DjangoCsvFetcher.create_club(csv_object)
        else:
            assert 0, "Wrong object to read: " + str(self._type)

    def read_file(self, file):
        with open(file, 'rt', encoding='utf-8') as csv_file:
            # reader2 = csv.reader(csv_file, delimiter=';')
            reader1, reader2 = itertools.tee(csv.reader(csv_file, delimiter=';'))
            columns = len(next(reader1))
            del reader1
            print('\nDetected %s columns\n' % columns)
            print('\nStarting reading {:n} from {:s}\n'.format(self._type, file))
            for row in reader2:
                if any(row):
                    if row[0] == self._fexit:
                        print(self._exit_text)
                        break
                    self.print_row_to_read(row)
                    csv_object = self.get_csv_object(row)
                    self.create_django_object(csv_object)
        csv_file.close()
        print('\nFinished reading {:s}...[0=PHASE, 1=TOURNAMENT, 2=NTS_STADISTIC]\n'.format(str(self._type)))
