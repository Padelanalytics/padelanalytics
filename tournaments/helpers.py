# Coppyright (c) 2016 - 2025 Francisco Javier Revilla Linares
# All rights reserved.

"""Tools, methods, utilities for the logic of views.py

This script contains different methods and classes mainly used in the views.py. All the logic to
calculate the groups, teams points, and how to represents it into the frontend are located here.
Other useful methods like dates, or converting data formats are here to find.
"""

import collections
import logging

from tournaments.models import GameRound, Team


logger = logging.getLogger(__name__)


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
            raise ValueError(
                "Argument columns_number must be a positive integer. Received : %s"
                % (columns_number)
            )
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
        n_rows = (
            len(local_players)
            if len(local_players) > len(visitor_players)
            else len(visitor_players)
        )
        for i in range(n_rows):
            if i < len(local_players):
                points = 0
                number = local_players[i].number if local_players[i].number else ""
                for st in stadistics:
                    if st.player == local_players[i]:
                        points = st.points
                        break
                if points > 0:
                    row = [number, local_players[i].person, points]
                else:
                    row = [number, local_players[i].person, "-"]
            else:
                row = ["", "", ""]
            if i < len(visitor_players):
                points = 0
                number = visitor_players[i].number if visitor_players[i].number else ""
                for st in stadistics:
                    if st.player == visitor_players[i]:
                        points = st.points
                        break
                if points > 0:
                    row.extend([number, visitor_players[i].person, points])
                else:
                    row.extend([number, visitor_players[i].person, "-"])
            else:
                row.extend(["", "", ""])

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
    plus_minus_games = 0
    defeated = list()

    def __repr__(self):
        return "%s p:%d w:%d l:%d d%d +:%d -:%d +/-:%d pts:%d" % (
            self.team,
            self.played,
            self.won,
            self.lost,
            self.drawn,
            self.plus,
            self.minus,
            self.plus_minus,
            self.points,
        )

    def __str__(self):
        return self.__repr__

    def __lt__(self, other):
        if self.phase.category == other.phase.category:
            if self.phase.round == other.phase.round:
                if self.points == other.points:
                    if self.plus_minus == other.plus_minus:
                        if self.plus_minus_games == other.plus_minus_games:
                            return other.team.id not in self.defeated
                        else:
                            return self.plus_minus_games < other.plus_minus_games
                    else:
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
                    if self.plus_minus == other.plus_minus:
                        return self.plus_minus_games <= other.plus_minus_games
                    else:
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
                return self.phase.round.cmp(other.phase.round)

        else:
            return self.phase.category.__cmp__(other.phase.category)

    def __init__(self, team: Team, phase: GameRound):
        self.team: Team = team
        self.phase: GameRound = phase

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
        elif self.phase.round == GameRound.POOL_D:
            return -1
        elif other == GameRound.POOL_D:
            return 1
        elif self.phase.round == GameRound.POOL_E:
            return -1
        elif other == GameRound.POOL_E:
            return 1
        elif self.phase.round == GameRound.POOL_F:
            return -1
        elif other == GameRound.POOL_F:
            return 1
        else:
            raise Exception(
                "Game.Round combination (%s, %s) is not allowed." % (self.phase.round, other)
            )

    def add_game(self, game):
        if game.local.id == self.team.id:
            if game.local_score < 0:
                self.won = 0
                self.points = 0
                return
            if game.local_score > game.visitor_score:
                self.won += 1
                self.points += WIN_POINTS(game)
                self.defeated.append(game.visitor.id)
            elif game.local_score < game.visitor_score:
                self.lost += 1
                self.points += LOST_POINTS(game)
            elif game.local_score == game.visitor_score:
                self.drawn += 1
                self.points += DRAW_POINTS(game)
            else:
                raise Exception("Wrong score for game %s" % (game))
            self.plus += game.local_score
            self.minus += game.visitor_score
            self.plus_minus += game.local_score - game.visitor_score
            self.plus_minus_games += game.result_padel.get_local_games_diff()
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
                raise Exception("Wrong score for game %s" % (game))
            self.plus += game.visitor_score
            self.minus += game.local_score
            self.plus_minus += game.visitor_score - game.local_score
            self.plus_minus_games += game.result_padel.get_visitor_games_diff()
        else:
            raise Exception("Expected team %s in the game but not found." % (self.team))
        self.played += 1


class NationsClassificationRow:
    played = 0
    points = 0
    defeated = list()
    won = 0
    lost = 0
    drawn = 0
    mplus = 0  # matches
    mminus = 0
    match_plus_minus = 0
    splus = 0  # sets
    sminus = 0
    set_plus_minus = 0
    games_plus_minus = 0  # games

    def __repr__(self):
        return "p:{}, w:{}, l:{}, d:{}, m+:{}, m-:{}, s+:{}, s-:{}".format(
            self.played,
            self.won,
            self.lost,
            self.drawn,
            self.mplus,
            self.mminus,
            self.splus,
            self.sminus,
        )

    def __str__(self):
        return self.__repr__

    def __lt__(self, other):
        if self.phase.category == other.phase.category:
            if self.phase.round == other.phase.round:
                if self.points == other.points:
                    if self.match_plus_minus == other.match_plus_minus:
                        if self.set_plus_minus == other.set_plus_minus:
                            if self.games_plus_minus == other.games_plus_minus:
                                return other.team.id not in self.defeated
                            else:
                                return self.games_plus_minus < other.games_plus_minus
                    else:
                        return self.set_plus_minus < other.set_plus_minus
                else:
                    return self.points < other.points
            else:
                return self.phase.round.__lt__(other.phase.round)
        else:
            return self.phase.category.__lt__(other.phase.category)

    def __le__(self, other):
        if self.phase.category == other.phase.category:
            if self.phase.round == other.phase.round:
                if self.points == other.points:
                    if self.match_plus_minus == other.match_plus_minus:
                        if self.set_plus_minus == other.set_plus_minus:
                            return self.games_plus_minus <= other.games_plus_minus
                        else:
                            return self.set_plus_minus <= other.set_plus_minus
                    else:
                        return self.match_plus_minus <= other.match_plus_minus
                else:
                    return self.points <= other.points
            else:
                return self.phase.round.__le__(other.phase.round)

    def __init__(self, team, phase):
        self.team = team
        self.phase = phase

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
        elif self.phase.round == GameRound.POOL_D:
            return -1
        elif other == GameRound.POOL_D:
            return 1
        elif self.phase.round == GameRound.POOL_E:
            return -1
        elif other == GameRound.POOL_E:
            return 1
        elif self.phase.round == GameRound.POOL_F:
            return -1
        elif other == GameRound.POOL_F:
            return 1
        else:
            raise Exception(
                "Game.Round combination (%s, %s) is not allowed." % (self.phase.round, other)
            )

    def add_game(self, game):
        if game.local.id == self.team.id:
            if game.local_score < 0:
                self.won = 0
                self.points = 0
                return
            if game.local_score > game.visitor_score:
                self.won += 1
                self.points += WIN_POINTS(game)
                self.defeated.append(game.visitor.id)
            elif game.local_score < game.visitor_score:
                self.lost += 1
                self.points += LOST_POINTS(game)
            elif game.local_score == game.visitor_score:
                self.drawn += 1
                self.points += DRAW_POINTS(game)
            else:
                raise ValueError("Wrong score for game %s" % (game))

            for g in game.games:
                if g.result_padel.winner == 1:
                    self.mplus += 1
                elif g.result_padel.winner == 2:
                    self.mminus += 1
                else:
                    raise ValueError("No existe el empate")
                self.splus += g.local_score
                self.sminus += g.visitor_score
                self.games_plus_minus = g.result_padel.get_local_games_diff()

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
                raise ValueError("Wrong score for game %s" % (game))

            for g in game.games:
                if g.result_padel.winner == 2:
                    self.mplus += 1
                elif g.result_padel.winner == 1:
                    self.mminus += 1
                else:
                    raise ValueError("No existe el empate")
                self.splus += g.visitor_score
                self.sminus += g.local_score
                self.games_plus_minus = g.result_padel.get_local_games_diff()

        else:
            raise ValueError

        self.played += 1

    def add_games(self, games):
        victories = 0
        defeats = 0

        for game in games:
            if game.local.id == self.team.id:
                if game.local_score < game.visitor_score:
                    defeats += 1
                    self.mminus += 1
                elif game.local_score > game.visitor_score:
                    victories += 1
                    self.mplus += 1
                elif game.local_score == game.visitor_score:
                    pass
                else:
                    raise ValueError("Wrong score for game %s" % (game))
                self.splus += game.local_score
                self.sminus += game.visitor_score
                self.games_plus_minus += game.result_padel.get_local_games_diff()

            elif game.visitor.id == self.team.id:
                if game.local_score < game.visitor_score:
                    victories += 1
                    self.mplus += 1
                elif game.local_score > game.visitor_score:
                    defeats += 1
                    self.mminus += 1
                elif game.local_score == game.visitor_score:
                    pass
                else:
                    raise ValueError("Wrong score for game %s" % (game))
                self.splus += game.visitor_score
                self.sminus += game.local_score
                self.games_plus_minus += game.result_padel.get_visitor_games_diff()

        # calculate points
        self.played += 1
        if victories > defeats:
            self.won += 1
            self.points += WIN_POINTS(game)
            self.defeated.append(game.visitor.id)
        elif victories < defeats:
            self.lost += 1
            self.points += LOST_POINTS(game)
        elif victories == defeats:
            self.drawn += 1
            self.points += DRAW_POINTS(game)


class NationsFixtures2:
    games = {}
    liga_games = {}
    pool_games = {}
    playoff_games = {}

    def __init__(self, games):
        self.games = {}
        self.liga_games = {}
        self.pool_games = {}
        self.playoff_games = {}

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

    def __create_rows(self, games):
        result = {}
        for game in games.values():
            key = str(game.local.id) + str(game.phase)
            if key in result:
                row = result.get(key)
                row.add_game(game)
            else:
                row = NationsClassificationRow(game.local, game.phase)
                row.add_game(game)

            result.update({key: row})

            key = str(game.visitor.id) + str(game.phase)
            if key in result:
                row = result.get(key)
                row.add_game(game)
            else:
                row = NationsClassificationRow(game.visitor, game.phase)
                row.add_game(game)

            result.update({key: row})

        return result

    def __sort_rows(self, rows):
        result = {}
        aux = sorted(rows.values(), reverse=True)
        if len(aux) == 0:
            return []

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

    def get_finals(self, result):
        result = {}
        for key in self.games:
            if key.round in [
                GameRound.FINAL,
                GameRound.SEMI,
                GameRound.QUARTER,
                GameRound.EIGHTH,
                GameRound.SIXTEENTH,
                GameRound.THIRD_POSITION,
                GameRound.FIFTH_POSITION,
                GameRound.SIXTH_POSITION,
                GameRound.SEVENTH_POSITION,
                GameRound.EIGHTH_POSITION,
                GameRound.NINTH_POSITION,
                GameRound.TENTH_POSITION,
                GameRound.ELEVENTH_POSITION,
                GameRound.TWELFTH_POSITION,
                GameRound.THIRTEENTH_POSITION,
                GameRound.FOURTEENTH_POSITION,
                GameRound.FIFTEENTH_POSITION,
                GameRound.SIXTEENTH_POSITION,
                GameRound.EIGHTEENTH_POSITION,
                GameRound.TWENTIETH_POSITION,
            ]:
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
            if result.get(GameRound.PREVIA):
                sorted_result[GameRound.PREVIA] = result[GameRound.PREVIA]
            if result.get(GameRound.PREPREVIA):
                sorted_result[GameRound.PREPREVIA] = result[GameRound.PREPREVIA]
            if result.get(GameRound.SILVER):
                sorted_result[GameRound.SILVER] = result[GameRound.SILVER]
            if result.get(GameRound.BRONZE):
                sorted_result[GameRound.BRONZE] = result[GameRound.BRONZE]
            if result.get(GameRound.WOOD):
                sorted_result[GameRound.WOOD] = result[GameRound.WOOD]
                #        return collections.OrderedDict(sorted(result))
        return sorted_result


class Fixtures:
    liga_games = {}
    pool_games = {}
    playoff_games = {}
    pool_rows = {}
    sorted_pools = {}
    games = {}
    liga_games = {}
    division_games = {}
    division_rows = {}
    pool_games = {}
    sorted_pools = {}
    sorted_divisions = {}

    def __init__(self, games):
        self.liga_games = {}
        self.pool_games = {}
        self.playoff_games = {}
        self.pool_rows = {}
        self.sorted_pools = {}
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
            return []

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
        self.sorted_divisions = collections.OrderedDict(
            sorted(self.sorted_divisions.items(), reverse=True)
        )

    def get_finals(self, result):
        result = {}
        for key in self.games:
            if (
                key.round == GameRound.FINAL
                or key.round == GameRound.SEMI
                or key.round == GameRound.QUARTER
                or key.round == GameRound.EIGHTH
                or key.round == GameRound.SIXTEENTH
                or key.round == GameRound.THIRD_POSITION
                or key.round == GameRound.FIFTH_POSITION
                or key.round == GameRound.SIXTH_POSITION
                or key.round == GameRound.SEVENTH_POSITION
                or key.round == GameRound.EIGHTH_POSITION
                or key.round == GameRound.NINTH_POSITION
                or key.round == GameRound.TENTH_POSITION
                or key.round == GameRound.ELEVENTH_POSITION
                or key.round == GameRound.TWELFTH_POSITION
                or key.round == GameRound.THIRTEENTH_POSITION
                or key.round == GameRound.FOURTEENTH_POSITION
                or key.round == GameRound.FIFTEENTH_POSITION
                or key.round == GameRound.SIXTEENTH_POSITION
                or key.round == GameRound.EIGHTEENTH_POSITION
                or key.round == GameRound.TWENTIETH_POSITION
            ):
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
            if result.get(GameRound.PREVIA):
                sorted_result[GameRound.PREVIA] = result[GameRound.PREVIA]
            if result.get(GameRound.PREPREVIA):
                sorted_result[GameRound.PREPREVIA] = result[GameRound.PREPREVIA]
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
            raise ValueError(
                "Argument columns_number must be a positive integer. Received : %s"
                % (columns_number)
            )
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


class NationsGame:
    local_score = 0
    visitor_score = 0
    games = []

    def __check_game(self, game):
        teams = [self.local, self.visitor]

        if game.local not in teams or game.visitor not in teams:
            raise ValueError("Games belong to more than two teams.")

    def __init__(self, games):
        for g in games:
            self.__check_game(g)
            if g.padel_result.winner == 1 and g.local == self.local:
                self.local_score += 1
            elif g.padel_result.winner == 2 and g.visitor == self.local:
                self.local_score += 1
            elif g.padel_result.winner == 1 and g.local == self.visitor:
                self.visitor_score += 1
            elif g.padel_result.winner == 2 and g.visitor == self.visitor:
                self.visitor_score += 1

        self.local = games[0].local
        self.visitor = games[0].visitor
        self.phase = games[0].phase
        self.games.extend(games)

    def get_score_str(self):
        return "{} - {}".format(str(self.local_score), str(self.visitor_score))

    def get_local(self):
        return self.local

    def get_visitor(self):
        return self.visitor

    def __lt__(self, other):
        return self.games[0].__lt__(other.games[0])

    def __cmp__(self, other):
        return self.games[0].__cmp__(other.games[0])


def sort_tournament_list(tournament_list, tournament_type):
    if tournament_type == "PADEL":
        return tournament_list

    result = {
        "England": list(),
        "World_Cup": list(),
        "Euros": list(),
        "Germany": list(),
        "Australia": list(),
    }
    for t in tournament_list:
        if "NTS" in t.name:
            result["England"].append(t)
        elif "World Cup" in t.name:
            result["World_Cup"].append(t)
        elif "Capital Cup" in t.name or "Championship 2016" == t.name:
            result["Germany"].append(t)
        elif "NTL" in t.name:
            result["Australia"].append(t)
        elif t.name in ["Euros 2014", "Euros 2016"]:
            result["Euros"].append(t)
        else:
            raise Exception("Tournament name %s not recognized." % t.name)
    result["England"] = sorted(
        result.get("England"), key=lambda tournament: tournament.date, reverse=True
    )
    result["World_Cup"] = sorted(
        result.get("World_Cup"),
        key=lambda tournament: tournament.name + tournament.division,
    )
    result["Australia"] = sorted(
        result.get("Australia"),
        key=lambda tournament: tournament.name + tournament.division,
    )
    result["Germany"] = sorted(
        result.get("Germany"),
        key=lambda tournament: tournament.name + tournament.division,
        reverse=True,
    )
    result["Euros"] = sorted(
        result.get("Euros"),
        key=lambda tournament: tournament.name + tournament.division,
        reverse=True,
    )
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
