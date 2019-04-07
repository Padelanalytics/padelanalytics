from tournaments.models import GameRound

import collections

import logging

from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


def last_monday(date = None):
    from datetime import datetime, timedelta
    if date:
        d = date
    else:
        d = datetime.now().date()
    d -= timedelta(days=d.weekday())
    return d


def all_mondays_from(d, tuple=False):
    """
    Returns all the mondays from the given date d until the last monday of the
    current year where the operatym system runs
    """
    result = []
    if d.weekday() != 0:
        d += timedelta(days=7-d.weekday())
    current_year = datetime.now().year
    while d.year <= current_year:
        result.append((d, d)) if tuple else result.append(d)
        d += timedelta(days=7)
    return result


def all_mondays_until(d, tuple=False):
    """
    Returns all the mondays from the given date d until the last monday of the current
    date where the operatym system runs.
    """
    result = []
    last_m = last_monday()
    if d.weekday() != 0:
        d += timedelta(days=7-d.weekday())
    while d <= last_m:
        result.append((d, d)) if tuple else result.append(d)
        d += timedelta(days=7)
    return result


def all_mondays_since(year):
    current_year = datetime.now().year
    d = datetime.date(year, 1, 1)                      # First January
    d += timedelta(days=(7-d.weekday()) % 7)  # First Monday
    while year <= d.year <= current_year:
        yield (d, d)
        d += timedelta(days=7)


class StructuresUtils:

    def get_team_view_games(self, games):
        result = {}
        for game in games:
            if game.phase in result:
                phase_games = result.get(game.phase)
            else:
                phase_games = []
            phase_games.append(game)
            result.update({game.phase: phase_games})
        return result

    def get_teams_matrix(self, teams, columns_number):
        if not (columns_number > 0):
            raise ValueError('Argument columns_number must be a positive integer. Received : %s' % (columns_number))
        column_size = len(teams) / columns_number
        if len(teams) % column_size > 0:
            column_size += 1
        column_size = int(column_size)

        #        matrix = [[0 for x in xrange(column_size)] for x in xrange(columns_number)]
        matrix = []
        for x in range(column_size):
            matrix.append([])
        i = 0
        for team in teams:
            matrix[i % column_size].append(team)
            i += 1
        return matrix

    def get_game_details_matrix(self, stadistics, local_players, visitor_players):
        result = []
        n_rows = len(local_players) if len(local_players) > len(visitor_players) else len(visitor_players)
        for i in range(n_rows):
            if i < len(local_players):
                points = 0
                number = local_players[i].number if local_players[i].number else ''
                for st in stadistics:
                    if st.player == local_players[i]:
                        points = st.points
                        break
                if points > 0:
                    row = [number, local_players[i].person, points]
                else:
                    row = [number, local_players[i].person, '-']
            else:
                row = ['', '', '']
            if i < len(visitor_players):
                points = 0
                number = visitor_players[i].number if visitor_players[i].number else ''
                for st in stadistics:
                    if st.player == visitor_players[i]:
                        points = st.points
                        break
                if points > 0:
                    row.extend([number, visitor_players[i].person, points])
                else:
                    row.extend([number, visitor_players[i].person, '-'])
            else:
                row.extend(['', '', ''])

            result.append(row)
        return result

    def get_team_details_matrix(self, stadistics, players):
        result = []
        for player in players:
            points = 0
            for st in stadistics:
                if st.player == player:
                    points += st.points
            result.append([player.number, player.person, points])
        return result


class ClassificationRow:
    played = 0
    won = 0
    lost = 0
    drawn = 0
    plus = 0
    minus = 0
    plus_minus = 0
    points = 0

    def __repr__(self):
        return '%s p:%d  w:%d l:%d d%d +:%d -:%d +/-:%d pts:%d' % (
            self.team, self.played, self.won, self.lost, self.drawn, self.plus, self.minus, self.plus_minus,
            self.points)

    def __str__(self):
        return '%s p:%d  w:%d l:%d d%d +:%d -:%d +/-:%d pts:%d' % (
            self.team, self.played, self.won, self.lost, self.drawn, self.plus, self.minus, self.plus_minus,
            self.points)

    def __lt__(self, other):
        if self.phase.category == other.phase.category:
            if self.phase.round == other.phase.round:
                if self.points == other.points:
                    return self.plus_minus < other.plus_minus
                else:
                    return self.points < other.points
            else:
                # return re.sub("\W+", "", self.phase.round.lower()).__cmp__(re.sub("\W+", "", other.phase.round))
                # return cmp(re.sub("\W+", "", self.phase.round.lower()), re.sub("\W+", "", other.phase.round)))
                # print('cmp_round(%s, %s) return %s.' % (self.phase.round, other.phase.round, self.cmp_round(other.phase.round)))
                return self.phase.round.__lt__(other.phase.round)
        else:
            return self.phase.category.__lt__(other.phase.category)

    def __le__(self, other):
        if self.phase.category == other.phase.category:
            if self.phase.round == other.phase.round:
                if self.points == other.points:
                    return self.plus_minus <= other.plus_minus
                else:
                    return self.points <= other.points
            else:
                # return re.sub("\W+", "", self.phase.round.lower()).__cmp__(re.sub("\W+", "", other.phase.round))
                # return cmp(re.sub("\W+", "", self.phase.round.lower()), re.sub("\W+", "", other.phase.round)))
                # print('cmp_round(%s, %s) return %s.' % (self.phase.round, other.phase.round, self.cmp_round(other.phase.round)))
                return self.phase.round.__le__(other.phase.round)
        else:
            return self.phase.category.__le__(other.phase.category)

    def __cmp__(self, other):
        if self.phase.category == other.phase.category:
            if self.phase.round == other.phase.round:
                if self.points == other.points:
                    return self.plus_minus.__cmp__(other.plus_minus)
                else:
                    return self.points.__cmp__(other.points)
            else:
                # return re.sub("\W+", "", self.phase.round.lower()).__cmp__(re.sub("\W+", "", other.phase.round))
                # return cmp(re.sub("\W+", "", self.phase.round.lower()), re.sub("\W+", "", other.phase.round)))
                # print('cmp_round(%s, %s) return %s.' % (self.phase.round, other.phase.round, self.cmp_round(other.phase.round)))
                return cmp(self.phase.round, other.phase.round)

        else:
            return self.phase.category.__cmp__(other.phase.category)

    def __init__(self, team, phase):
        self.team = team
        self.phase = phase

    def __eq__(self, other):
        self.team.id == other.team.id

    def cmp_round(self, other):
        if self.phase.round == other:
            return 0
        elif self.phase.round == GameRound.POOL_A:
            return -1
        elif other == GameRound.POOL_A:
            return 1
        elif self.phase.round == GameRound.POOL_B:
            return -1
        elif other == GameRound.POOL_B:
            return 1
        elif self.phase.round == GameRound.POOL_C:
            return -1
        elif other == GameRound.POOL_C:
            return 1
        else:
            raise Exception('Game.Round combination (%s, %s) is not allowed.' % (self.phase.round, other))

    def add_game(self, game):
        if game.local.id == self.team.id:
            if game.local_score < 0:
                self.won = 0
                self.points = 0
                return
            if game.local_score > game.visitor_score:
                self.won += 1
                self.points += WIN_POINTS(game)
            elif game.local_score < game.visitor_score:
                self.lost += 1
                self.points += LOST_POINTS(game)
            elif game.local_score == game.visitor_score:
                self.drawn += 1
                self.points += DRAW_POINTS(game)
            else:
                raise Exception('Wrong score for game %s' % (game))
            self.plus += game.local_score
            self.minus += game.visitor_score
            self.plus_minus += game.local_score - game.visitor_score
        elif game.visitor.id == self.team.id:
            if game.visitor_score < 0:
                self.won = 0
                self.points = 0
                return
            if game.local_score < game.visitor_score:
                self.won += 1
                self.points += WIN_POINTS(game)
            elif game.local_score > game.visitor_score:
                self.lost += 1
                self.points += LOST_POINTS(game)
            elif game.local_score == game.visitor_score:
                self.drawn += 1
                self.points += DRAW_POINTS(game)
            else:
                raise Exception('Wrong score for game %s' % (game))
            self.plus += game.visitor_score
            self.minus += game.local_score
            self.plus_minus += game.visitor_score - game.local_score
        else:
            raise Exception('Expected team %s in the game but not found.' % (self.team))
        self.played += 1


class Fixtures:
    liga_games = {}
    pool_games = {}
    playoff_games = {}
    pool_rows = {}
    sorted_pools = {}

    def __init__(self, games):
        self.games = {}
        self.liga_games = {}
        self.division_games = {}
        self.division_rows = {}
        self.pool_games = {}
        self.sorted_pools = {}
        self.sorted_divisions = {}

        for game in games:
            # split games in different rounds
            if game.phase.round == GameRound.LIGA:
                self.liga_games.update({game.id: game})
            elif GameRound.is_pool(game.phase):
                self.pool_games.update({game.id: game})
            else:
                self.playoff_games.update({game.id: game})

            if game.phase in self.games:
                phase_games = self.games.get(game.phase)
                phase_games.update({game.id: game})
            else:
                self.games.update({game.phase: {game.id: game}})

        # create classification rows
        self.pool_rows = self.__create_rows(self.pool_games)
        self.sorted_pools = self.__sort_rows(self.pool_rows)
        self.liga_rows = self.__create_rows(self.liga_games)
        self.sorted_ligas = self.__sort_rows(self.liga_rows)
        self.__sort_divisions()

    def __create_rows(self, games):
        result = {}
        for game in games.values():
            key = str(game.local.id) + str(game.phase)
            if key in result:
                row = result.get(key)
                row.add_game(game)
            else:
                row = ClassificationRow(game.local, game.phase)
                row.add_game(game)

            result.update({key: row})

            key = str(game.visitor.id) + str(game.phase)
            if key in result:
                row = result.get(key)
                row.add_game(game)
            else:
                row = ClassificationRow(game.visitor, game.phase)
                row.add_game(game)

            result.update({key: row})

        return result

    def __sort_rows(self, rows):
        result = {}
        aux = sorted(rows.values(), reverse=True)
        if len(aux) == 0:
            return[]

        row_list = []
        old_round = aux[0].phase.round
        for item in aux:
            new_round = item.phase.round
            if old_round != new_round:
                row_list = []
            row_list.append(item)
            result.update({item.phase.round: row_list})
            old_round = new_round

        result = collections.OrderedDict(sorted(result.items()))
        return result

    def __sort_divisions(self):
        for k, v in self.games.items():
            if k.round == GameRound.DIVISION:
                self.division_games.update({k: v})

        for k, v in self.division_games.items():
            division_rows = self.__create_rows(v)
            self.sorted_divisions[k] = self.__sort_rows(division_rows)
        self.sorted_divisions = collections.OrderedDict(sorted(self.sorted_divisions.items(), reverse=True))

    def get_finals(self, result):
        result = {}
        for key in self.games:
            if (key.round == GameRound.FINAL or
            key.round == GameRound.SEMI or
            key.round == GameRound.QUARTER or
            key.round == GameRound.EIGHTH or
            key.round == GameRound.SIXTEENTH or
            key.round == GameRound.THIRD_POSITION or
            key.round == GameRound.FIFTH_POSITION or
            key.round == GameRound.SIXTH_POSITION or
            key.round == GameRound.SEVENTH_POSITION or
            key.round == GameRound.EIGHTH_POSITION or
            key.round == GameRound.NINTH_POSITION or
            key.round == GameRound.TENTH_POSITION or
            key.round == GameRound.ELEVENTH_POSITION or
            key.round == GameRound.TWELFTH_POSITION or
            key.round == GameRound.THIRTEENTH_POSITION or
            key.round == GameRound.FOURTEENTH_POSITION or
            key.round == GameRound.FIFTEENTH_POSITION or
            key.round == GameRound.SIXTEENTH_POSITION or
            key.round == GameRound.EIGHTEENTH_POSITION or
            key.round == GameRound.TWENTIETH_POSITION):
                result[key] = self.games[key]
                # result.update({key:self.games[key]})
                # return sorted(result.values(), reverse=True)
        for k1, v1 in result.items():
            result[k1] = collections.OrderedDict(sorted(v1.items()))

        return collections.OrderedDict(sorted(result.items()))

    def get_phased_finals(self, result):
        result = {}
        sorted_result = collections.OrderedDict()
        finals = self.get_finals({})
        old_phase = GameRound.GOLD
        variable = {}
        for key in finals:
            if key.category != old_phase:
                variable = {}
                old_phase = key.category
            variable.update({key: finals[key]})
            # result.update({key.category:variable})
            result.update({key.category: collections.OrderedDict(sorted(variable.items()))})
        if result:
            if result.get(GameRound.GOLD):
                sorted_result[GameRound.GOLD] = result[GameRound.GOLD]
            if result.get(GameRound.SILVER):
                sorted_result[GameRound.SILVER] = result[GameRound.SILVER]
            if result.get(GameRound.BRONZE):
                sorted_result[GameRound.BRONZE] = result[GameRound.BRONZE]
            if result.get(GameRound.WOOD):
                sorted_result[GameRound.WOOD] = result[GameRound.WOOD]
                #        return collections.OrderedDict(sorted(result))
        return sorted_result


class TeamsMatrix:
    matrix = []

    def __init__(self, columns_number, teams):
        if not (columns_number > 0):
            raise ValueError('Argument columns_number must be a positive integer. Received : %s' % (columns_number))
        # self.teams_matrix[columns_numbers][]
        self.matrix = []
        column_size = len(teams) / columns_number
        column = []
        i = 0
        for team in teams:
            column.append(team)
            if i == column_size - 1:
                i = 0
                self.matrix.append(column)
                column = []
            else:
                i += 1


def sort_tournament_list(tournament_list, tournament_type):
    if tournament_type == "PADEL":
        return tournament_list

    result = {"England": list(), "World_Cup": list(), "Euros": list(), "Germany": list(), "Australia": list()}
    for t in tournament_list:
        if 'NTS' in t.name:
            result["England"].append(t)
        elif 'World Cup' in t.name:
            result["World_Cup"].append(t)
        elif 'Capital Cup' in t.name or 'Championship 2016' == t.name:
            result["Germany"].append(t)
        elif 'NTL' in t.name:
            result["Australia"].append(t)
        elif t.name in ['Euros 2014', 'Euros 2016']:
            result["Euros"].append(t)
        else:
            raise Exception('Tournament name %s not recognized.' % t.name)
    result["England"] = sorted(result.get("England"), key=lambda tournament: tournament.date, reverse=True)
    result["World_Cup"] = sorted(result.get("World_Cup"), key=lambda tournament: tournament.name+tournament.division)
    result["Australia"] = sorted(result.get("Australia"), key=lambda tournament: tournament.name+tournament.division)
    result["Germany"] = sorted(result.get("Germany"), key=lambda tournament: tournament.name+tournament.division, reverse=True)
    result["Euros"] = sorted(result.get("Euros"), key=lambda tournament: tournament.name+tournament.division, reverse=True)
    return result


def WIN_POINTS(game):
    if game.tournament.name == "NTL 2016" or "NTS" in game.tournament.name:
        return 4
    else:
        return 3


def DRAW_POINTS(game):
        return 2


def LOST_POINTS(game):
    if game.tournament.name == "NTL 2016":
        return 0
    else:
        return 1


