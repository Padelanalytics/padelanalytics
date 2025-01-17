import crypt
from datetime import datetime
from time import strftime

import pycountry

from tournaments import csvdata


def hashing():
    return crypt.crypt()


class DrawError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class PadelResult:
    def __init__(self, scores):
        self._asset_init(scores)
        self.scores = scores
        self.local_score = []
        self.visitor_score = []
        for x in range(0, len(scores)):
            try:
                score = int(scores[x])
                if scores[x] == "" or score < 0 or score > 20:
                    raise ValueError
                if x % 2 == 0:
                    self.local_score.append(score)
                else:
                    self.visitor_score.append(score)
            except ValueError:
                pass

    def get_local_score(self):
        sets = 0
        for x in range(0, len(self.local_score)):
            if self.local_score[x] > self.visitor_score[x]:
                sets += 1
        return sets

    def get_visitor_score(self):
        sets = 0
        for x in range(0, len(self.visitor_score)):
            if self.visitor_score[x] > self.local_score[x]:
                sets += 1
        return sets

    def is_draw(self):
        """Returns True if the result is a draw otherwise False."""
        try:
            return self.get_winner() == 0
        except DrawError:
            return True
        return False

    def get_winner(self, allow_draw=True):
        """Returns: 1 if local team won, 2 if visitor team won, 0 if is a draw or an exception if draw is not allowed"""
        local_sets = self.get_local_score()
        visitor_sets = self.get_visitor_score()
        if local_sets > visitor_sets:
            return 1
        elif local_sets < visitor_sets:
            return 2
        else:
            if allow_draw:
                return 0
            raise DrawError("The game is a draw.")

    def _asset_init(self, scores):
        assert len(scores) % 2 == 0, "Scores list argument length must be modulo 2."

        for score in scores[:-1]:
            if score and not isinstance(int(score), int):
                raise ValueError("Scores argument must be list of integers.")

    def __str__(self):
        return str(self.scores)


class PadelTeamNames:
    is_nations = False
    is_clubs = False
    local_country = None
    visitor_country = None

    def __init__(self, csv):
        if len(csv) != 10:
            raise ValueError("Touch games has a local and a visitor names")
        for name in csv:
            if not isinstance(name, str):
                raise ValueError("Names must be a string.")

        self.local_first_first_name = csv[3]
        self.local_first_last_name = csv[2]
        self.local_second_first_name = csv[5]
        self.local_second_last_name = csv[4]

        self.visitor_first_first_name = csv[7]
        self.visitor_first_last_name = csv[6]
        self.visitor_second_first_name = csv[9]
        self.visitor_second_last_name = csv[8]

        # if there is no team name:
        if 0 == len(csv[0]) and 0 == len(csv[1]):
            # order alphabetically by surname to avoid duplicates teams
            if self.local_first_last_name <= self.local_second_last_name:
                self.local = self.local_first_last_name + " - " + self.local_second_last_name
            else:
                self.local = self.local_second_last_name + " - " + self.local_first_last_name

            if self.visitor_first_last_name <= self.visitor_second_last_name:
                self.visitor = (
                    self.visitor_first_last_name + " - " + self.visitor_second_last_name
                )
            else:
                self.visitor = (
                    self.visitor_second_last_name + " - " + self.visitor_first_last_name
                )
        else:  # if there is a team name (nations or clubs):
            # nations or club name
            self.local = csv[0]
            self.visitor = csv[1]
            self.is_multicountry = True
            try:
                if self.local == "Basque Country" or self.visitor_country == "Basque Country":
                    self.local_country = self.local
                    self.visitor_country = pycountry.countries.search_fuzzy(csv[1])[0].alpha_3
                elif self.visitor == "Basque Country":
                    self.local_country = pycountry.countries.search_fuzzy(csv[0])[0].alpha_3
                    self.visitor_country = self.visitor
                else:
                    self.local_country = pycountry.countries.search_fuzzy(csv[0])[0].alpha_3
                    self.visitor_country = pycountry.countries.search_fuzzy(csv[1])[0].alpha_3

                self.is_nations = True
            except Exception:
                # raise ValueError('The country does not exists.')
                self.local_country = csv[0]
                self.visitor_country = csv[1]
                self.is_clubs = True

            # pair team
            # order alphabetically by surname to avoid duplicates teams
            if self.local_first_last_name <= self.local_second_last_name:
                self.sublocal = (
                    self.local_first_last_name + " - " + self.local_second_last_name
                )
            else:
                self.sublocal = (
                    self.local_second_last_name + " - " + self.local_first_last_name
                )

            if self.visitor_first_last_name <= self.visitor_second_last_name:
                self.subvisitor = (
                    self.visitor_first_last_name + " - " + self.visitor_second_last_name
                )
            else:
                self.subvisitor = (
                    self.visitor_second_last_name + " - " + self.visitor_first_last_name
                )

    def is_multigame(self):
        return self.is_nations or self.is_clubs


class Game:
    def __init__(self):
        self.local = self.visitor = self.padel_team_names = None
        self.round = self.category = self.nteams = None
        self.tournament_name = self.division = self.result = None
        self.date_time = self.field = None

    def get_local_score(self):
        return self.result.get_local_score()

    def get_visitor_score(self):
        return self.result.get_visitor_score()

    def get_result(self):
        return self.result

    def set_local(self, local):
        self.local = local

    def get_winner(self):
        return self.result.get_winner()

    def is_draw(self):
        return self.is_draw()

    def get_date(self):
        return strftime("%m/%d/%y", self.date_time)

    def get_time(self):
        return strftime("%H:%M", self.date_time)

    def is_multigame(self):
        return self.padel_team_names.is_multigame()

    def is_nations(self):
        return self.padel_team_names.is_nations

    def is_clubs(self):
        return self.padel_team_names.is_clubs

    def get_touch_csv_list(self):
        result = list(range(14))
        result[csvdata.TG_TOURNAMENT_INDEX] = self.tournament_name
        result[csvdata.TG_DIVISION_INDEX] = self.division
        result[csvdata.TG_DATE_INDEX] = self.get_date()
        result[csvdata.TG_TIME_INDEX] = self.get_time()
        result[csvdata.TG_FIELD_INDEX] = self.field
        result[csvdata.TG_PHASE_INDEX] = self.round
        result[csvdata.TG_CATEGORY_INDEX] = self.category
        result[csvdata.TG_PHASE_TEAMS_INDEX] = self.n_teams
        result[9] = "xx"
        result[csvdata.TG_LOCAL_TEAM_INDEX] = self.local
        result[csvdata.TG_LOCAL_TEAM_SCORE_INDEX] = self.local_score
        result[csvdata.TG_VISITOR_TEAM_SCORE_INDEX] = self.visitor_score
        result[csvdata.TG_VISITOR_TEAM_INDEX] = self.visitor
        return result

    @classmethod
    def padel_from_csv_list(cls, csv):
        game = cls()
        game.federation = csv[0]
        game.tournament_name = csv[1]
        game.ranking = csv[2]
        game.division = csv[3]
        # game.date_time = datetime.strptime(csv[3], '%d/%m/%y')
        game.date_time = datetime.strptime(csv[4], "%d.%m.%Y")
        # game.date = strftime("%m/%d/%y", game.date_time)
        # game.time = None
        # 4 => time , 5 => field
        game.round = csv[7]
        game.category = csv[8]
        game.nteams = csv[9]
        game.padel_team_names = PadelTeamNames(csv[10:20])
        game.local = game.padel_team_names.local
        game.visitor = game.padel_team_names.visitor
        game.padel_result = PadelResult(csv[21:])
        game.local_score = game.padel_result.get_local_score()
        game.visitor_score = game.padel_result.get_visitor_score()
        game.sublocal = None
        game.subvisitor = None
        game.local_country = game.padel_team_names.local_country
        game.visitor_country = game.padel_team_names.visitor_country
        if 0 == len(csv[10]) and 0 == len(csv[11]):
            game.is_pair = True
        else:
            game.is_pair = False
            game.sublocal = game.padel_team_names.sublocal
            game.subvisitor = game.padel_team_names.subvisitor

        return game
