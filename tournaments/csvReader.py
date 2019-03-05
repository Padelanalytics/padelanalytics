import csv
import logging

import itertools

from tournaments.models import PadelRanking
from tournaments import games
from tournaments import csvdata
from tournaments.models import Game
from tournaments.models import PadelResult
from tournaments.models import GameField
from tournaments.models import GameRound
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
            print('Created {:s}:\n'.format(type(obj).__name__) + str(obj))
            logger.debug('Created {:s}:\n'.format(type(obj).__name__) + str(obj))

        else:
            if obj is None:
                print('Neither object found or created.\n')
                logger.debug('Neither object found or created.\n')
            else:
                print('Found {:s}:\n'.format(type(obj).__name__) + str(obj))
                logger.debug('Found {:s}:\n'.format(type(obj).__name__) + str(obj))

    @staticmethod
    def get_or_create_tournament(tournament_name, tournament_division, type, ranking=None):
        result = Tournament.objects.get_or_create(
            name=tournament_name, division=tournament_division, type=type, padel_serie=ranking)
        return result

    @staticmethod
    def get_team(team_name, division):
        return Team.objects.get(name=team_name, division=division)

    @staticmethod
    def get_or_create_team(team_name, team_division):
        result = Team.objects.get_or_create(name=team_name, division=team_division)
        return result

    @staticmethod
    def get_or_create_person(first_name, last_name, gender=None, nationality=None, born=None):
        try:
            result = Person.objects.get(first_name=first_name, last_name=last_name)
            update = False
            if gender and result.gender is None:
                result.gender = gender
                Person.objects.get(first_name=first_name, last_name=last_name).update(gender=gender)
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
            if gender:
                result = Person.objects.get(first_name=first_name, last_name=last_name, gender=gender)
                result = result, False
        except ObjectDoesNotExist:
            if gender:
                result = Person.objects.get_or_create(first_name=first_name, last_name=last_name, gender=gender)
            else:
                result = Person.objects.get_or_create(first_name=first_name, last_name=last_name)
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
    def blablabla(ranking, monday, person):
        try:
            obj = PadelRanking.objects.get(country=ranking.country, date=monday, circuit=ranking.circuit,
                                           division=ranking.division, person=person.id)
            obj.points = ranking.points
            obj.save(force_update=True)
        except PadelRanking.DoesNotExist:
            obj = PadelRanking.objects.create(country=ranking.country, date=monday, circuit=ranking.circuit,
                                              division=ranking.division, person=person, points=ranking.points)
        return obj


    @staticmethod
    def get_or_create_padel_ranking(ranking):
        from datetime import datetime
        person, b = DjangoCsvFetcher.create_padel_person(ranking)
        mondays = all_mondays_from(datetime.strptime(ranking.date, "%Y-%m-%d"))
        for monday in mondays:
            obj = DjangoSimpleFetcher.blablabla(ranking, monday, person)
        return obj, True


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

    def create_padel_person(ranking):
        gender = get_player_gender(ranking.division)
        person = DjangoSimpleFetcher.get_or_create_person(
            first_name=ranking.first_name, last_name=ranking.last_name, gender=gender)
        return person

    def create_padel_persons(game, local_team, visitor_team, tournament_id):
        if game.padel_team_names:
            gender = get_player_gender(game.division)
            # local team first pair
            person, created = DjangoSimpleFetcher.get_or_create_person(
                    game.padel_team_names.local_first_first_name,
                    game.padel_team_names.local_first_last_name,
                    gender)
            DjangoSimpleFetcher.print_fetch_result(person, created)
            DjangoSimpleFetcher.get_or_create_player(person, local_team, None, tournament_id)
            # local team second pair
            person, created = DjangoSimpleFetcher.get_or_create_person(
                    game.padel_team_names.local_second_first_name,
                    game.padel_team_names.local_second_last_name,
                    gender)
            DjangoSimpleFetcher.print_fetch_result(person, created)
            DjangoSimpleFetcher.get_or_create_player(person, local_team, None, tournament_id)
            # visitor team first pair
            person, created = DjangoSimpleFetcher.get_or_create_person(
                    game.padel_team_names.visitor_first_first_name,
                    game.padel_team_names.visitor_first_last_name,
                    gender)
            DjangoSimpleFetcher.print_fetch_result(person, created)
            DjangoSimpleFetcher.get_or_create_player(person, visitor_team, None, tournament_id)
            # visitor team second pair
            person, created = DjangoSimpleFetcher.get_or_create_person(
                    game.padel_team_names.visitor_second_first_name,
                    game.padel_team_names.visitor_second_last_name,
                    gender)
            DjangoSimpleFetcher.print_fetch_result(person, created)
            DjangoSimpleFetcher.get_or_create_player(person, visitor_team, None, tournament_id)

    @staticmethod
    def create_padel_csv_game(game):
        type = "PADEL"

        tournament, created = DjangoSimpleFetcher.get_or_create_tournament(
            game.tournament_name, game.division, type, game.ranking)
        DjangoSimpleFetcher.print_fetch_result(tournament, created)

        local_team, created = create_or_fetch_team(game.local, game.division)
        DjangoSimpleFetcher.print_fetch_result(local_team, created)

        add_team_to_tournament(tournament, local_team)
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

        DjangoCsvFetcher.create_padel_persons(game, local_team, visitor_team, tournament.id)
        padel_result = game.padel_result

        game, created = DjangoSimpleFetcher.create_game(
                tournament, phase, field, time, local_team, visitor_team,
                game.local_score, game.visitor_score, padel_result)
        DjangoSimpleFetcher.print_fetch_result(game, created)

    @staticmethod
    def create_touch_csv_game(game):
        # if not isinstance(game, csvdata.CsvGame):
        #    assert 0, "Wrong game to read: " + game
        type = "TOUCH"
        padel_result = None

        tournament, created = DjangoSimpleFetcher.get_or_create_tournament(game.tournament_name, game.division, type)
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


def printCF(obj, created):
    if obj:
        if created:
            print('Created {:s}:\n {:s}'.format(obj.__class__.__name__, obj))
        else:
            print('Found {:s}:\n {:s}'.format(obj.__class__.__name__, obj))
    else:
        print('ERROR\n')


class CsvReader:
    (PHASE, TOURNAMENT, NTS_STATISTIC, FIT_STATISTIC, PADEL_GAME, PERSON, PADEL_RANKING) = (0, 1, 2, 3, 4, 5, 6)

    def __init__(self, type):
        if type in [self.PHASE, self.TOURNAMENT, self.NTS_STATISTIC, self.FIT_STATISTIC, self.PADEL_GAME, self.PERSON,
                    self.PADEL_RANKING]:
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
            DjangoSimpleFetcher.get_or_create_padel_ranking(csv_object)
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
