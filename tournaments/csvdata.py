from time import strftime
from tournaments.models import MO, M40, WO, W27, MXO, SMX


def get_tournament_url(tournament):
    if tournament == WC_2015_MO_GAMES_FOX:
        return remote_files_WC2015_MO_FOX
    elif tournament == WC_2015_WO_GAMES_FOX:
        return remote_files_WC2015_WO_FOX
    elif tournament == WC_2015_MXO_GAMES_FOX:
        return remote_files_WC2015_MXO_FOX
    elif tournament == WC_2015_SMX_GAMES_FOX:
        return remote_files_WC2015_SMX_FOX
    elif tournament == WC_2015_W27_GAMES_FOX:
        return remote_files_WC2015_W27_FOX
    elif tournament == WC_2015_M30_GAMES_FOX:
        return remote_files_WC2015_M30_FOX
    elif tournament == NTL_2016_MO_GAMES_FOX:
        return remote_files_NTL2016_MO_FOX
    elif tournament == NTL_2016_WO_GAMES_FOX:
        return remote_files_NTL2016_WO_FOX
    elif tournament == EUROS_2014_MO:
        return remote_files_EUROS_2014_MO
    elif tournament == EUROS_2014_WO:
        return remote_files_EUROS_2014_WO
    elif tournament == EUROS_2014_MXO:
        return remote_files_EUROS_2014_MXO
    elif tournament == EUROS_2014_W27:
        return remote_files_EUROS_2014_W27
    elif tournament == EUROS_2014_SMX:
        return remote_files_EUROS_2014_SMX
    elif tournament == EUROS_2014_M40:
        return remote_files_EUROS_2014_M40
    elif tournament == EUROS_2016_MO:
        return remote_files_EUROS_2016_MO
    elif tournament == EUROS_2016_WO:
        return remote_files_EUROS_2016_WO
    elif tournament == EUROS_2016_MXO:
        return remote_files_EUROS_2016_MXO
    elif tournament == EUROS_2016_W27:
        return remote_files_EUROS_2016_W27
    elif tournament == EUROS_2016_SMX:
        return remote_files_EUROS_2016_SMX
    else:
        raise ValueError("Tournament not supported.")


def get_fit_remote_stats_files(tournament):
    competition = get_competition(tournament)
    division = get_tournament_division(tournament)
    return remote_fit_stats_files.get(competition).get(division)


def get_fit_local_stats_files(tournament):
    competition = get_competition(tournament)
    division = get_tournament_division(tournament)
    return local_fit_stats_files.get(competition).get(division)


def get_tournament_html_path(tournament):
    if tournament == WC_2015_MO_GAMES_FOX:
        return local_files_WC_2015_MO_FX
    elif tournament == WC_2015_WO_GAMES_FOX:
        return local_files_WC_2015_WO_FX
    elif tournament == WC_2015_MXO_GAMES_FOX:
        return local_files_WC_2015_MXO_FX
    elif tournament == WC_2015_SMX_GAMES_FOX:
        return local_files_WC_2015_SMX_FX
    elif tournament == WC_2015_W27_GAMES_FOX:
        return local_files_WC_2015_W27_FX
    elif tournament == WC_2015_M30_GAMES_FOX:
        return local_files_WC_2015_M30_FX
    elif tournament == NTL_2016_MO_GAMES_FOX:
        return local_files_NTL_2016_M_FX
    elif tournament == NTL_2016_WO_GAMES_FOX:
        return local_files_NTL_2016_WO_FX
    elif tournament == EUROS_2014_MO:
        return local_files_EUROS_2014_MO
    elif tournament == EUROS_2014_WO:
        return local_files_EUROS_2014_WO
    elif tournament == EUROS_2014_MXO:
        return local_files_EUROS_2014_MXO
    elif tournament == EUROS_2014_SMX:
        return local_files_EUROS_2014_SMX
    elif tournament == EUROS_2014_W27:
        return local_files_EUROS_2014_W27
    elif tournament == EUROS_2014_M40:
        return local_files_EUROS_2014_M40
    elif tournament == EUROS_2016_MO:
        return local_files_EUROS_2016_MO
    elif tournament == EUROS_2016_WO:
        return local_files_EUROS_2016_WO
    elif tournament == EUROS_2016_MXO:
        return local_files_EUROS_2016_MXO
    elif tournament == EUROS_2016_SMX:
        return local_files_EUROS_2016_SMX
    elif tournament == EUROS_2016_W27:
        return local_files_EUROS_2016_W27

    else:
        raise ValueError("Tournament not supported.")


def get_csv_path(tournament, is_stats=False, is_test=True):
    if tournament == WC_2015_MO_GAMES_FOX:
        filename = 'WC_2015_MO_GAMES_FOX'
    elif tournament == WC_2015_M30_GAMES_FOX:
        filename = 'WC_2015_M30_GAMES_FOX'
    elif tournament == WC_2015_WO_GAMES_FOX:
        filename = 'WC_2015_WO_GAMES_FOX'
    elif tournament == WC_2015_W27_GAMES_FOX:
        filename = 'WC_2015_W27_GAMES_FOX'
    elif tournament == WC_2015_MXO_GAMES_FOX:
        filename = 'WC_2015_MXO_GAMES_FOX'
    elif tournament == WC_2015_SMX_GAMES_FOX:
        filename = 'WC_2015_SMX_GAMES_FOX'
    elif tournament == NTL_2016_MO_GAMES_FOX:
        filename = 'NTL_2016_MO_GAMES_FOX'
    elif tournament == NTL_2016_WO_GAMES_FOX:
        filename = 'NTL_2016_WO_GAMES_FOX'
    elif tournament == WC_2015_MO_GAMES_FIT:
        filename = 'WC_2015_MO_GAMES_FIT'
    elif tournament == WC_2015_WO_GAMES_FIT:
        filename = 'WC_2015_WO_GAMES_FIT'
    elif tournament == WC_2015_MXO_GAMES_FIT:
        filename = 'WC_2015_MXO_GAMES_FIT'
    elif tournament == EUROS_2014_MO:
        filename = 'EUROS_2014_MO_GAMES_FIT'
    elif tournament == EUROS_2014_WO:
        filename = 'EUROS_2014_WO_GAMES_FIT'
    elif tournament == EUROS_2014_MXO:
        filename = 'EUROS_2014_MXO_GAMES_FIT'
    elif tournament == EUROS_2014_W27:
        filename = 'EUROS_2014_W27_GAMES_FIT'
    elif tournament == EUROS_2014_SMX:
        filename = 'EUROS_2014_SMX_GAMES_FIT'
    elif tournament == EUROS_2014_M40:
        filename = 'EUROS_2014_M40_GAMES_FIT'
    elif tournament == EUROS_2016_MO:
        filename = 'EUROS_2016_MO_GAMES_FIT'
    elif tournament == EUROS_2016_WO:
        filename = 'EUROS_2016_WO_GAMES_FIT'
    elif tournament == EUROS_2016_MXO:
        filename = 'EUROS_2016_MXO_GAMES_FIT'
    elif tournament == EUROS_2016_W27:
        filename = 'EUROS_2016_W27_GAMES_FIT'
    elif tournament == EUROS_2016_SMX:
        filename = 'EUROS_2016_SMX_GAMES_FIT'
    else:
        raise ValueError('Illegal argument: %s', tournament)

    if is_stats:
        filename = filename.replace('GAMES', 'STATS')

    filename = CSV_FILES + filename + '.csv'

    if is_test:
        filename += '.test'

    return filename


def get_tournament_name(tournament):
    if tournament in [WC_2015_MO_GAMES_FOX, WC_2015_WO_GAMES_FOX, WC_2015_MXO_GAMES_FOX, WC_2015_SMX_GAMES_FOX,
                      WC_2015_W27_GAMES_FOX, WC_2015_M30_GAMES_FOX]:
        return 'World Cup 2015'
    elif tournament in [NTL_2016_MO_GAMES_FOX, NTL_2016_WO_GAMES_FOX]:
        return 'NTL 2016'
    elif tournament in [EUROS_2014_MO, EUROS_2014_M40, EUROS_2014_WO, EUROS_2014_W27, EUROS_2014_MXO, EUROS_2014_SMX]:
        return 'Euros 2014'
    elif tournament in [EUROS_2016_MO, EUROS_2016_WO, EUROS_2016_W27, EUROS_2016_MXO, EUROS_2016_SMX]:
        return 'Euros 2016'
    else:
        raise ValueError("Tournament not supported.")


def get_tournament_division(tournament):
    if tournament in [WC_2015_MO_GAMES_FOX, EUROS_2014_MO, EUROS_2014_M40, EUROS_2016_MO, NTL_2016_MO_GAMES_FOX]:
        return 'MO'
    elif tournament == WC_2015_M30_GAMES_FOX:
        return 'M30'
    elif tournament == EUROS_2014_M40:
        return 'M40'
    elif tournament in [WC_2015_WO_GAMES_FOX, NTL_2016_WO_GAMES_FOX, EUROS_2014_WO, EUROS_2016_WO]:
        return 'WO'
    elif tournament in [WC_2015_W27_GAMES_FOX, EUROS_2014_W27, EUROS_2016_W27]:
        return 'W27'
    elif tournament in [WC_2015_MXO_GAMES_FOX, EUROS_2014_MXO, EUROS_2016_MXO]:
        return 'MXO'
    elif tournament in [WC_2015_SMX_GAMES_FOX, EUROS_2014_SMX, EUROS_2016_SMX]:
        return 'SMX'
    else:
        raise ValueError("Tournament not supported.")


def get_competition(tournament):
    if tournament in [EUROS_2014_WO, EUROS_2014_W27, EUROS_2014_MO, EUROS_2014_M40, EUROS_2014_MXO, EUROS_2014_SMX]:
        return EUROS_2014
    elif tournament in [EUROS_2016_WO, EUROS_2016_W27, EUROS_2016_MO, EUROS_2016_MXO, EUROS_2016_SMX]:
        return EUROS_2016
    else:
        raise ValueError("Tournament not supported.")


def get_tournament_year(tournament):
    if tournament in [WC_2015_MO_GAMES_FOX, WC_2015_WO_GAMES_FOX, WC_2015_MXO_GAMES_FOX, WC_2015_SMX_GAMES_FOX,
                      WC_2015_W27_GAMES_FOX, WC_2015_M30_GAMES_FOX]:
        return 2015
    elif tournament in [NTL_2016_MO_GAMES_FOX, NTL_2016_WO_GAMES_FOX, EUROS_2016_MO, EUROS_2016_WO, EUROS_2016_MXO,
                        EUROS_2016_W27, EUROS_2016_SMX]:
        return 2016
    elif tournament in [EUROS_2014_MO, EUROS_2014_WO, EUROS_2014_MXO, EUROS_2014_W27, EUROS_2014_SMX, EUROS_2014_M40]:
        return 2014
    else:
        raise ValueError("Tournament not supported.")


class FitStatistic:
    def __init__(self, tournament_name, division, team, player_number, first_name, last_name, gender, played, scores,
                 mvp):
        self.tournament_name = tournament_name
        self.division = division
        self.team = team
        self.number = player_number
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.played = played
        self.scores = scores
        self.mvp = mvp

    @classmethod
    def from_array(cls, row):
        return cls(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9])


class CsvNTSStatistic:
    def __init__(self, row, tname=None, division=None, team=None, number=None, first_name=None, last_name=None,
                 gender=None, tries=None, mvp=None, local=None, local_score=None, visitor_score=None, visitor=None,
                 category=None, round=None, team_numbers=None):
        if row:
            self._tournament_name = row[PL_ST_TOURNAMENT_INDEX]
            self._division = row[PL_ST_DIVISION_INDEX]
            self._team = row[PL_ST_TEAM_INDEX]
            self._number = row[PL_ST_NUMBER_INDEX]
            self._first_name = row[PL_ST_FIRST_NAME_INDEX]
            self._last_name = row[PL_ST_LAST_NAME_INDEX]
            self._gender = row[PL_ST_GENDER_INDEX]
            self._tries = row[PL_ST_PLAYER_TRIES_INDEX]
            self._mvp = row[PL_ST_PLAYER_MVP_INDEX]
            self._local = row[PL_ST_LOCAL_TEAM_INDEX]
            self._local_score = row[PL_ST_LOCAL_TEAM_SCORE_INDEX]
            self._visitor_score = row[PL_ST_VISITOR_TEAM_SCORE_INDEX]
            self._visitor = row[PL_ST_VISITOR_TEAM_INDEX]
            self._category = row[PL_ST_GAME_CATEGORY_INDEX]
            self._round = row[PL_ST_GAME_ROUND_INDEX]
            self._team_numbers = row[PL_ST_PHASE_TEAMS_INDEX]
        else:
            self._tournament_name = tname
            self._division = division
            self._team = team
            self._number = number
            self._first_name = first_name
            self._last_name = last_name
            self._gender = gender
            self._tries = tries
            self._mvp = mvp
            self._local = local
            self._local_score = local_score
            self._visitor_score = visitor_score
            self._visitor = visitor
            self._category = category
            self._round = round
            self._team_numbers = team_numbers

    @property
    def tournament_name(self):
        return self._tournament_name

    @tournament_name.setter
    def tournament_name(self, tournament_name):
        self._tournament_name = tournament_name

    @property
    def division(self):
        return self._division

    @division.setter
    def division(self, division):
        self._division = division

    @property
    def team(self):
        return self._team

    @team.setter
    def team(self, team):
        self._team = team

    @property
    def number(self):
        return self._number

    @number.setter
    def number(self, number):
        self._number = number

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, first_name):
        self._first_name = first_name

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, last_name):
        self._last_name = last_name

    @property
    def gender(self):
        return self._gender

    @gender.setter
    def gender(self, gender):
        self._gender = gender

    @property
    def tries(self):
        return self._tries

    @tries.setter
    def tries(self, tries):
        self._tries = tries

    @property
    def mvp(self):
        return self.mvp

    @mvp.setter
    def mvp(self, mvp):
        self._mvp = mvp

    @property
    def local(self):
        return self._local

    @local.setter
    def local(self, local):
        self._local = local

    @property
    def local_score(self):
        return self._local_score

    @local_score.setter
    def local_score(self, local_score):
        self._local_score = local_score

    @property
    def visitor_score(self):
        return self._visitor_score

    @visitor_score.setter
    def visitor_score(self, visitor_score):
        self._visitor_score = visitor_score

    @property
    def visitor(self):
        return self._visitor

    @visitor.setter
    def visitor(self, visitor):
        self._visitor = visitor

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, category):
        self._category = category

    @property
    def round(self):
        # print(self._round.encode('UTF-8'))
        if self._round.encode('UTF-8') == b'\xc2\xbc':
            result = '1/4'
        else:
            result = self._round
        return result

    @round.setter
    def round(self, round):
        self._round = round

    @property
    def team_numbers(self):
        return self._team_numbers

    @team_numbers.setter
    def team_numbers(self, team_numbers):
        self._team_numbers = team_numbers

    def to_csv_array(self):
        result = list(range(15))
        result[PL_ST_TOURNAMENT_INDEX] = self._tournament_name
        result[PL_ST_DIVISION_INDEX] = self._division
        result[PL_ST_TEAM_INDEX] = self._team
        result[PL_ST_NUMBER_INDEX] = self._number
        result[PL_ST_FIRST_NAME_INDEX] = self._first_name
        result[PL_ST_LAST_NAME_INDEX] = self._last_name
        result[PL_ST_GENDER_INDEX] = self._gender
        result[PL_ST_PLAYER_TRIES_INDEX] = self._tries
        result[PL_ST_LOCAL_TEAM_INDEX] = self._local
        result[PL_ST_LOCAL_TEAM_SCORE_INDEX] = self._local_score
        result[PL_ST_VISITOR_TEAM_SCORE_INDEX] = self._visitor_score
        result[PL_ST_VISITOR_TEAM_INDEX] = self._visitor
        result[PL_ST_GAME_CATEGORY_INDEX] = self._category
        result[PL_ST_GAME_ROUND_INDEX] = self._round
        result[PL_ST_PHASE_TEAMS_INDEX] = self._team_numbers
        return result

    def to_csv_game(self):
        pass

    def __str__(self):
        return self.to_csv_array().__str__()


class CsvPhase:
    def __init__(self, row):
        self._category = row[PH_CATEGORY_INDEX]
        self._round = row[PH_PHASE_ROUND_INDEX]
        self._teams = row[PH_PHASE_TEAMS_INDEX]

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, category):
        self._category = category

    @property
    def round(self):
        if self._round.encode('UTF-8') == b'\xc2\xbc':
            result = '1/4'
        else:
            result = self._round
        return result

    @round.setter
    def round(self, round):
        self._round = round

    @property
    def teams(self):
        return self._teams

    @teams.setter
    def teams(self, teams):
        self._teams = teams

    def to_csv_array(self):
        result = list(range(3))
        result[PH_CATEGORY_INDEX] = self._category
        result[PH_PHASE_ROUND_INDEX] = self._round
        result[PH_PHASE_TEAMS_INDEX] = self._teams
        return result


class FitGame:
    def __init__(self, game, round=None, finals=None, nteams=None, date=None, time=None,
                 field=None, local=None, local_score=None, visitor_score=None, visitor=None):
        if game:
            self._round = game[0]
            self._finals = game[2]
            self._nteams = game[1]
            self._date = strftime("%m/%d/%y", game[3])
            self._time = strftime("%H:%M", game[3])
            self._timedate = game[3]
            self._field = game[4]
            self._local = game[5]
            self._local_score = game[6]
            self._visitor_score = game[7]
            self._visitor = game[8]
        else:
            self._round = round
            self._finals = finals
            self._nteams = nteams
            self._date = date
            self._time = time
            self._field = field
            self._local = local
            self._local_score = local_score
            self._visitor_score = visitor_score
            self._visitor = visitor

    def to_array(self):
        result = list(range(8))
        result[0] = self.round
        result[1] = self.nteams
        result[2] = self.finals
        result[3] = None
        result[4] = self.field
        result[5] = self.local
        result[6] = self.local_score
        result[7] = self.visitor_score
        result[8] = self.visitor

    @property
    def round(self):
        return self._round

    @round.setter
    def round(self, round):
        self._round = round

    @property
    def finals(self):
        return self._finals

    @finals.setter
    def finals(self, finals):
        self._finals = finals

    @property
    def nteams(self):
        return self._nteams

    @nteams.setter
    def nteams(self, nteams):
        self._nteams = nteams

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, date):
        self._date = date

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, time):
        self._time = time

    @property
    def field(self):
        return self._field

    @field.setter
    def field(self, field):
        self._field = field

    @property
    def local(self):
        return self._local

    @local.setter
    def local(self, local):
        self._local = local

    @property
    def visitor(self):
        return self._visitor

    @visitor.setter
    def visitor(self, visitor):
        self._visitor = visitor

    @property
    def local_score(self):
        return self._local_score

    @local_score.setter
    def local_score(self, local_score):
        self._local_score = local_score

    @property
    def visitor_score(self):
        return self._visitor_score

    @visitor_score.setter
    def visitor_score(self, visitor_score):
        self._visitor_score = visitor_score


class CsvGame(FitGame):
    def __init__(self, row, game, tournament_name, division):
        if row is None:
            super().__init__(None, game.round, game.finals, game.nteams, game.date, game.time, game.field,
                             game.local, game.local_score, game.visitor_score, game.visitor)

            self._tournament_name = tournament_name
            self._division = division
            self._category = 'Gold'

            if game.round == 'Division 2':
                self._category = 'Silver'
            elif game.round == 'Division 3':
                self._category = 'Bronze'
            elif 'Seeding' in game.round:
                self._category = 'Silver'
            else:
                self._category = 'Gold'

            if 'Division' in game.round:
                self._round = 'Division'
            elif 'finals' == game.round:
                self._round = game.finals
                self._round = self._round.replace('Grand Final', 'Final', 1)
                self._round = self._round.replace('Playoff 5th/6th', FIFTH_POSITION, 1)
                self._round = self._round.replace('5th/6th Playoff', FIFTH_POSITION, 1)
                self._round = self._round.replace('5th/6th Seeding', FIFTH_POSITION, 1)
                self._round = self._round.replace('Playoff 6th/7th', SIXTH_POSITION, 1)
                self._round = self._round.replace('Playoff 7th/8th', SEVENTH_POSITION, 1)
                self._round = self._round.replace('7th/8th Playoff', SEVENTH_POSITION, 1)
                self._round = self._round.replace('7th/8th Seeding', SEVENTH_POSITION, 1)
                self._round = self._round.replace('Playoff 8th/9th', EIGHTH_POSITION, 1)
                self._round = self._round.replace('Playoff 9th/10th', NINTH_POSITION, 1)
                self._round = self._round.replace('9th/10th/11th', NINTH_POSITION, 1)
                self._round = self._round.replace('Playoff 10th/11th', TENTH_POSITION, 1)
                self._round = self._round.replace('Playoff 11th/12th', ELEVENTH_POSITION, 1)
                self._round = self._round.replace('Playoff 12th/13th', TWELFTH_POSITION, 1)
                self._round = self._round.replace('Playoff 13th/14th', THIRTEENTH_POSITION, 1)
                self._round = self._round.replace('Playoff 14th/15th', FOURTEENTH_POSITION, 1)
                self._round = self._round.replace('Playoff 15th/16th', FIFTEENTH_POSITION, 1)
                self._round = self._round.replace('Playoff 16th/17th', SIXTEENTH_POSITION, 1)
                self._round = self._round.replace('Playoff 18th/19th', EIGHTEENTH_POSITION, 1)
                self._round = self._round.replace('Playoff 20th/21st', TWENTIETH_POSITION, 1)
                self._round = self._round.replace('Bronze Final', THIRD_POSITION, 1)
                self._round = self._round.replace('Bronze', THIRD_POSITION, 1)
                self._round = self._round.replace('Seeding Semi Final 1', 'Semifinal', 1)
                self._round = self._round.replace('Seeding Semi Final 2', 'Semifinal', 1)
            else:
                self._round = game.round
        else:
            super(CsvGame, self).__init__(None, row[TG_PHASE_INDEX], None, row[TG_PHASE_TEAMS_INDEX],
                                          row[TG_DATE_INDEX], row[TG_TIME_INDEX], row[TG_FIELD_INDEX],
                                          row[TG_LOCAL_TEAM_INDEX], row[TG_LOCAL_TEAM_SCORE_INDEX],
                                          row[TG_VISITOR_TEAM_SCORE_INDEX], row[TG_VISITOR_TEAM_INDEX])
            self._tournament_name = row[TG_TOURNAMENT_INDEX]
            self._division = row[TG_DIVISION_INDEX]
            self._category = row[TG_CATEGORY_INDEX]

    @classmethod
    def from_scratch(cls, t_name, division, date, time, field, phase, category, team_number, local, local_score,
                     visitor_score, visitor):
        row = list(range(13))
        row[TG_TOURNAMENT_INDEX] = t_name
        row[TG_DIVISION_INDEX] = division
        row[TG_DATE_INDEX] = date
        row[TG_TIME_INDEX] = time
        row[TG_FIELD_INDEX] = field
        row[TG_PHASE_INDEX] = cls.parse_phase(phase)
        row[TG_CATEGORY_INDEX] = category
        row[TG_PHASE_TEAMS_INDEX] = team_number
        row[TG_LOCAL_TEAM_INDEX] = local
        row[TG_LOCAL_TEAM_SCORE_INDEX] = local_score
        row[TG_VISITOR_TEAM_SCORE_INDEX] = visitor_score
        row[TG_VISITOR_TEAM_INDEX] = visitor
        return cls(row, None, None, None)

    @staticmethod
    def parse_phase(phase_name):
        result = phase_name
        if phase_name in ROUNDS_CONVERSIONS:
            result = ROUNDS_CONVERSIONS[phase_name]
        return result

    @property
    def tournament_name(self):
        return self._tournament_name

    @tournament_name.setter
    def tournament_name(self, tournament_name):
        self._tournament_name = tournament_name

    @property
    def division(self):
        return self._division

    @division.setter
    def division(self, division):
        self._division = division

    @property
    def round(self):
        return self._round

    @round.setter
    def round(self, round):
        self._round = round

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, category):
        self._category = category

    def to_csv_array(self):
        result = list(range(13))
        result[TG_TOURNAMENT_INDEX] = self._tournament_name
        result[TG_DIVISION_INDEX] = self._division
        result[TG_DATE_INDEX] = self.date
        result[TG_TIME_INDEX] = self.time
        result[TG_FIELD_INDEX] = self._field
        result[TG_PHASE_INDEX] = self._round
        result[TG_CATEGORY_INDEX] = self._category
        result[TG_PHASE_TEAMS_INDEX] = self._nteams
        result[8] = 'xx'
        result[TG_LOCAL_TEAM_INDEX] = self._local
        result[TG_LOCAL_TEAM_SCORE_INDEX] = self._local_score
        result[TG_VISITOR_TEAM_SCORE_INDEX] = self._visitor_score
        result[TG_VISITOR_TEAM_INDEX] = self._visitor
        return result

    def __str__(self):
        return self.to_csv_array().__str__()

    def csv_len_standard(self):
        return 13

    def csv_len_tennis(self):
        return self.csv_len_standard() + 10


class FoxGame(CsvGame):
    def __init__(self, t_name, division, date, time, field, phase, category, team_number, local, local_score,
                 visitor_score, visitor, link):
        self._stats_link = link
        row = list(range(13))
        row[TG_TOURNAMENT_INDEX] = t_name
        row[TG_DIVISION_INDEX] = division
        row[TG_DATE_INDEX] = date
        row[TG_TIME_INDEX] = time
        row[TG_FIELD_INDEX] = field
        row[TG_PHASE_INDEX] = CsvGame.parse_phase(phase)
        row[TG_CATEGORY_INDEX] = category
        row[TG_PHASE_TEAMS_INDEX] = team_number
        row[TG_LOCAL_TEAM_INDEX] = local
        row[TG_LOCAL_TEAM_SCORE_INDEX] = local_score
        row[TG_VISITOR_TEAM_SCORE_INDEX] = visitor_score
        row[TG_VISITOR_TEAM_INDEX] = visitor
        super().__init__(row, None, None, None)

    @property
    def stats_link(self):
        return self._stats_link

    @stats_link.setter
    def link(self, stats_link):
        self._stats_link = stats_link

    def get_game_statistic_file_to_save(self):
        destination = self.tournament_name + '-' + self.division + '-' + self.date + '-' + self.time + '-' + self. \
            round + '-' + self.category + '-' + str(self.nteams) + '-' + self.local + '-' + str(
                self.local_score) + '-' + str(self.visitor_score) + '-' + self.visitor + '.html'

        destination = destination.replace(' ', '_')
        destination = destination.replace('/', '_')
        destination = destination.replace(':', '_')
        return RAW_STATS_FILES + destination


def create_person(row):
    from player.models import Person
    born = None
    nationality = None
    if row[0] is None or len(row[0]) == 0 or row[1] is None or len(row[1]) == 0 or row[4] is None or len(row[4]) == 0:
        raise ValueError("Invalid value at row: ", row)

    if row[2]:
        born = strftime("%y/%m/%d", row[2])
    if row[3]:
        nationality = row[3]

    person = Person(
        first_name=row[0],
        last_name=row[1],
        born=born,
        nationality=nationality,
        gender=row[4])

    return person


class Ranking:
    def __init__(self, country, circuit, division, first_name, last_name, date, points):
        self.country = country
        self.circuit = circuit
        self.division = division
        self.first_name = first_name
        self.last_name = last_name
        self.date = date
        self.points = points

    @classmethod
    def from_array(cls, row):
        return cls(row[0], row[1], row[2], row[3], row[4], row[5], row[6])


def create_padel_ranking(row):
    return Ranking.from_array(row)


# PHASES_INDEXES
PH_PHASE_ROUND_INDEX = 0
PH_CATEGORY_INDEX = 1
PH_PHASE_TEAMS_INDEX = 2

# TOURNAMENT_GAMES_INDEXES
TG_TOURNAMENT_INDEX = 0
TG_DIVISION_INDEX = 1
TG_DATE_INDEX = 2
TG_TIME_INDEX = 3
TG_FIELD_INDEX = 4
TG_PHASE_INDEX = 5
TG_CATEGORY_INDEX = 6
TG_PHASE_TEAMS_INDEX = 7
# TG_GAME_ROUND_INDEX = 8
TG_LOCAL_TEAM_INDEX = 9
TG_LOCAL_TEAM_SCORE_INDEX = 10
TG_VISITOR_TEAM_SCORE_INDEX = 11
TG_VISITOR_TEAM_INDEX = 12

# PLAYER_STATISTICS_INDEXES
PL_ST_TOURNAMENT_INDEX = 0
PL_ST_DIVISION_INDEX = 1
PL_ST_TEAM_INDEX = 2
PL_ST_NUMBER_INDEX = 3
PL_ST_FIRST_NAME_INDEX = 4
PL_ST_LAST_NAME_INDEX = 5
PL_ST_GENDER_INDEX = 6
PL_ST_PLAYER_TRIES_INDEX = 7
PL_ST_PLAYER_MVP_INDEX = 8
PL_ST_LOCAL_TEAM_INDEX = 9
PL_ST_LOCAL_TEAM_SCORE_INDEX = 10
PL_ST_VISITOR_TEAM_SCORE_INDEX = 11
PL_ST_VISITOR_TEAM_INDEX = 12
PL_ST_GAME_CATEGORY_INDEX = 13
PL_ST_GAME_ROUND_INDEX = 14
PL_ST_PHASE_TEAMS_INDEX = 15

# FOX GAMES INDEXES
FOX_GAME_STATISTIC_LINK_LINK = 10

# POSITION CONSTANTS CONVERSION
THIRD_POSITION = 'Third position'
FIFTH_POSITION = 'Fifth position'
SIXTH_POSITION = 'Sixth position'
SEVENTH_POSITION = 'Seventh position'
EIGHTH_POSITION = 'Eighth position'
NINTH_POSITION = 'Ninth position'
TENTH_POSITION = 'Tenth position'
ELEVENTH_POSITION = 'Eleventh position'
TWELFTH_POSITION = 'Twelfth position'
THIRTEENTH_POSITION = 'Thirteenth position'
FOURTEENTH_POSITION = 'Fourteenth position'
FIFTEENTH_POSITION = 'Fifteenth position'
SIXTEENTH_POSITION = 'Sixteenth position'
EIGHTEENTH_POSITION = 'Eighteenth position'
TWENTIETH_POSITION = 'Twentieth position'

ROUNDS_CONVERSIONS = {'Grand Final': 'Final',
                      'Gold Medal Game': 'Final',
                      'Bronze': THIRD_POSITION,
                      'Bronze Medal Game': THIRD_POSITION,
                      'Playoff 5th/6th': FIFTH_POSITION,
                      'Playoff 7th/8th': SEVENTH_POSITION,
                      'Playoff 8th/9th': EIGHTH_POSITION,
                      'Playoff 9th/10th': NINTH_POSITION,
                      'Playoff 10th/11th': TENTH_POSITION,
                      'Playoff 11th/12th': ELEVENTH_POSITION,
                      'Playoff 12th/13th': TWELFTH_POSITION,
                      'Playoff 13th/14th': THIRTEENTH_POSITION,
                      'Playoff 15th/16th': FIFTEENTH_POSITION,
                      'Playoff 18th/19th': EIGHTEENTH_POSITION,
                      'Playoff 20th/21st': TWENTIETH_POSITION,
                      'Playoff for 5th/6th': FIFTH_POSITION,
                      'Playoff for 7th/8th': SEVENTH_POSITION,
                      'Playoff for 11th/12th': ELEVENTH_POSITION,
                      'Playoff for 15th/16th': FIFTEENTH_POSITION,
                      'Plate Final': NINTH_POSITION,
                      'Playoff 9th/10th (Plate Final)': NINTH_POSITION,
                      'Playoff 16th/17th (Bowl Final)': SIXTEENTH_POSITION}

# CONSTANTS DIRECTORIES
DATA_FILES = './player/data_files/'
RAW_FILES = DATA_FILES + 'raw/'
RAW_GAMES_FILES = RAW_FILES + 'games/'
RAW_STATS_FILES = RAW_FILES + 'statistics/'
RAW_STATS_FILES_EUROS = RAW_FILES + 'statistics/euros/'
CSV_FILES = DATA_FILES + 'csv/'

# CONSTANTS FILE NAMES
GAME_PREFIX = 'TGames'
WC2015_MO_URL = 'http://www.internationaltouch.org/events/world-cup/2015/mens/'
WC2015_WO_URL = 'http://www.internationaltouch.org/events/world-cup/2015/womens/'
WC2015_MXO_URL = 'http://www.internationaltouch.org/events/world-cup/2015/mixed/'
WC2015_MO_FOX_RAW = RAW_FILES + 'WC2015_MO_FOX_RAW.html'
WC2015_WO_FOX_RAW = RAW_FILES + 'WC2015_WO_FOX_RAW.html'
WC2015_MXO_FOX_RAW = RAW_FILES + 'WC2015_MXO_FOX_RAW.html'
WC2015_MO_RAW = RAW_FILES + 'WC2015_MO_RAW.txt'
WC2015_WO_RAW = RAW_FILES + 'WC2015_WO_RAW.txt'
WC2015_MXO_RAW = RAW_FILES + 'WC2015_MX_RAW.txt'
WC2015_MO_CSV = CSV_FILES + GAME_PREFIX + '_WC2015_MO_RAW.csv'
WC2015_WO_CSV = CSV_FILES + GAME_PREFIX + '_WC2015_WO_RAW.csv'
WC2015_MXO_CSV = CSV_FILES + GAME_PREFIX + '_WC2015_MX_RAW.csv'
WC2015_MO_RAW = RAW_GAMES_FILES + 'WC2015_MO_RAW.txt'
WC2015_WO_RAW = RAW_GAMES_FILES + 'WC2015_WO_RAW.txt'
WC2015_MXO_RAW = RAW_GAMES_FILES + 'WC2015_MX_RAW.txt'
WC2015_MO_CSV = CSV_FILES + GAME_PREFIX + '_WC2015_MO_RAW.csv'
WC2015_WO_CSV = CSV_FILES + GAME_PREFIX + '_WC2015_WO_RAW.csv'
WC2015_MXO_CSV = CSV_FILES + GAME_PREFIX + '_WC2015_MX_RAW.csv'
EUROS2014_MO_CSV = CSV_FILES + GAME_PREFIX + '_EUROS2016_MO_RAW.csv'
WC2015_MO_URL = 'http://www.internationaltouch.org/events/world-cup/2015/mens/'
WC2015_WO_URL = 'http://www.internationaltouch.org/events/world-cup/2015/womens/'
WC2015_MXO_URL = 'http://www.internationaltouch.org/events/world-cup/2015/mixed/'
remote_files_WC2015_WO_FOX = [
    'http://www.foxsportspulse.com/comp_info.cgi?client=1-9035-0-360318-0&pool=11&action=ROUND&round=-1',
    'http://www.foxsportspulse.com/comp_info.cgi?client=1-9035-0-360318-0&pool=12&action=ROUND&round=-1',
    'http://www.foxsportspulse.com/comp_info.cgi?client=1-9035-0-360318-0&pool=13&action=ROUND&round=-1',
    'http://www.foxsportspulse.com/comp_info.cgi?client=1-9035-0-360318-0&pool=14&action=ROUND&round=-1',
    'http://www.foxsportspulse.com/comp_info.cgi?client=1-9035-0-360318-0&pool=21&action=ROUND&round=-1',
    'http://www.foxsportspulse.com/comp_info.cgi?client=1-9035-0-360318-0&pool=22&action=ROUND&round=-1',
    'http://www.foxsportspulse.com/comp_info.cgi?client=1-9035-0-360318-0&pool=1031&action=ROUND&round=-1',
    'http://www.foxsportspulse.com/comp_info.cgi?client=1-9035-0-360318-0&pool=1032&action=ROUND&round=-1']
remote_files_WC2015_WO_FOX = [
    'http://www.foxsportspulse.com/comp_info.cgi?client=1-9035-0-360318-0&pool=11&action=ROUND&round=-1',
    'http://www.foxsportspulse.com/comp_info.cgi?client=1-9035-0-360318-0&pool=12&action=ROUND&round=-1',
    'http://www.foxsportspulse.com/comp_info.cgi?client=1-9035-0-360318-0&pool=13&action=ROUND&round=-1',
    'http://www.foxsportspulse.com/comp_info.cgi?client=1-9035-0-360318-0&pool=14&action=ROUND&round=-1',
    'http://www.foxsportspulse.com/comp_info.cgi?client=1-9035-0-360318-0&pool=21&action=ROUND&round=-1',
    'http://www.foxsportspulse.com/comp_info.cgi?client=1-9035-0-360318-0&pool=22&action=ROUND&round=-1',
    'http://www.foxsportspulse.com/comp_info.cgi?client=1-9035-0-360318-0&pool=1031&action=ROUND&round=-1',
    'http://www.foxsportspulse.com/comp_info.cgi?client=1-9035-0-360318-0&pool=1032&action=ROUND&round=-1']
remote_files_WC2015_W27_FOX = [
    'http://www.foxsportspulse.com/comp_info.cgi?a=ROUND&round=-1&client=1-9035-0-360317-0&pool=11',
    'http://www.foxsportspulse.com/comp_info.cgi?client=1-9035-0-360317-0&pool=1012&action=ROUND&round=-1']
remote_files_WC2015_MO_FOX = [
    'http://www.foxsportspulse.com/comp_info.cgi?client=1-9035-0-360314-0&pool=11&action=ROUND&round=-1',
    'http://www.foxsportspulse.com/comp_info.cgi?client=1-9035-0-360314-0&pool=12&action=ROUND&round=-1',
    'http://www.foxsportspulse.com/comp_info.cgi?client=1-9035-0-360314-0&pool=13&action=ROUND&round=-1',
    'http://www.foxsportspulse.com/comp_info.cgi?client=1-9035-0-360314-0&pool=14&action=ROUND&round=-1',
    'http://www.foxsportspulse.com/comp_info.cgi?client=1-9035-0-360314-0&pool=21&action=ROUND&round=-1',
    'http://www.foxsportspulse.com/comp_info.cgi?client=1-9035-0-360314-0&pool=22&action=ROUND&round=-1',
    'http://www.foxsportspulse.com/comp_info.cgi?client=1-9035-0-360314-0&pool=1031&action=ROUND&round=-1',
    'http://www.foxsportspulse.com/comp_info.cgi?client=1-9035-0-360314-0&pool=1032&action=ROUND&round=-1']
remote_files_WC2015_MXO_FOX = [
    'http://www.foxsportspulse.com/comp_info.cgi?a=ROUND&round=-1&client=1-9035-0-360315-0&pool=11',
    'http://www.foxsportspulse.com/comp_info.cgi?client=1-9035-0-360315-0&pool=12&action=ROUND&round=-1',
    'http://www.foxsportspulse.com/comp_info.cgi?client=1-9035-0-360315-0&pool=13&action=ROUND&round=-1',
    'http://www.foxsportspulse.com/comp_info.cgi?client=1-9035-0-360315-0&pool=14&action=ROUND&round=-1',
    'http://www.foxsportspulse.com/comp_info.cgi?client=1-9035-0-360315-0&pool=15&action=ROUND&round=-1',
    'http://www.foxsportspulse.com/comp_info.cgi?client=1-9035-0-360315-0&pool=16&action=ROUND&round=-1',
    'http://www.foxsportspulse.com/comp_info.cgi?client=1-9035-0-360315-0&pool=21&action=ROUND&round=-1',
    'http://www.foxsportspulse.com/comp_info.cgi?client=1-9035-0-360315-0&pool=22&action=ROUND&round=-1',
    'http://www.foxsportspulse.com/comp_info.cgi?client=1-9035-0-360315-0&pool=23&action=ROUND&round=-1',
    'http://www.foxsportspulse.com/comp_info.cgi?client=1-9035-0-360315-0&pool=1031&action=ROUND&round=-1',
    'http://www.foxsportspulse.com/comp_info.cgi?client=1-9035-0-360315-0&pool=1032&action=ROUND&round=-1',
    'http://www.foxsportspulse.com/comp_info.cgi?client=1-9035-0-360315-0&pool=1033&action=ROUND&round=-1']
remote_files_WC2015_SMX_FOX = [
    'http://www.foxsportspulse.com/comp_info.cgi?client=1-9035-0-360319-0&pool=11&action=ROUND&round=-1#',
    'http://www.foxsportspulse.com/comp_info.cgi?client=1-9035-0-360319-0&pool=1013&action=ROUND&round=-1',
    'http://www.foxsportspulse.com/comp_info.cgi?client=1-9035-0-360319-0&pool=1012&action=ROUND&round=-1']
remote_files_WC2015_M30_FOX = [
    'http://www.foxsportspulse.com/comp_info.cgi?a=ROUND&round=-1&client=1-9035-0-360316-0&pool=11',
    'http://www.foxsportspulse.com/comp_info.cgi?client=1-9035-0-360316-0&pool=1012&action=ROUND&round=-1'
]
remote_files_NTL2016_MO_FOX = [
    'http://www.foxsportspulse.com/comp_info.cgi?client=14-907-0-402811-0&pool=1&action=ROUND&round=-1',
    'http://www.foxsportspulse.com/comp_info.cgi?client=14-907-0-402811-0&pool=1001&action=ROUND&round=-1'
]
remote_files_NTL2016_WO_FOX = [
    'http://www.foxsportspulse.com/comp_info.cgi?client=14-907-0-402794-0&pool=1&action=ROUND&round=-1',
    'http://www.foxsportspulse.com/comp_info.cgi?client=14-907-0-402794-0&pool=1001&action=ROUND&round=-1'
]
remote_files_EUROS_2014_MO = ['https://www.internationaltouch.org/events/euros/2014/mens-open/']
remote_files_EUROS_2014_WO = ['https://www.internationaltouch.org/events/euros/2014/womens-open/']
remote_files_EUROS_2014_MXO = ['https://www.internationaltouch.org/events/euros/2014/mixed-open/']
remote_files_EUROS_2014_SMX = ['https://www.internationaltouch.org/events/euros/2014/senior-mixed/']
remote_files_EUROS_2014_W27 = ['https://www.internationaltouch.org/events/euros/2014/womens-27/']
remote_files_EUROS_2014_M40 = ['https://www.internationaltouch.org/events/euros/2014/mens-40/']
remote_files_EUROS_2016_MO = ['https://www.internationaltouch.org/events/euros/2016/mens-open/']
remote_files_EUROS_2016_WO = ['https://www.internationaltouch.org/events/euros/2016/womens-open/']
remote_files_EUROS_2016_MXO = ['https://www.internationaltouch.org/events/euros/2016/mixed-open/']
remote_files_EUROS_2016_SMX = ['https://www.internationaltouch.org/events/euros/2016/senior-mixed/']
remote_files_EUROS_2016_W27 = ['https://www.internationaltouch.org/events/euros/2016/womens-27/']


local_files_WC_2015_MO_FX = [RAW_GAMES_FILES + 'WC2015_MO_FOX_POOLA.html',
                             RAW_GAMES_FILES + 'WC2015_MO_FOX_POOLB.html',
                             RAW_GAMES_FILES + 'WC2015_MO_FOX_POOLC.html',
                             RAW_GAMES_FILES + 'WC2015_MO_FOX_POOLD.html',
                             RAW_GAMES_FILES + 'WC2015_MO_FOX_DIVONE.html',
                             RAW_GAMES_FILES + 'WC2015_MO_FOX_DIVTWO.html',
                             RAW_GAMES_FILES + 'WC2015_MO_FOX_CHAMPIONSHIP.html',
                             RAW_GAMES_FILES + 'WC2015_MO_FOX_PLATE.html']

local_files_WC_2015_M30_FX = [RAW_GAMES_FILES + 'WC2015_M30_FOX_POOLA.html',
                              RAW_GAMES_FILES + 'WC2015_M30_FOX_CHAMPIONSHIP.html']

local_files_WC_2015_WO_FX = [RAW_GAMES_FILES + 'WC2015_WO_FOX_POOLA.html',
                             RAW_GAMES_FILES + 'WC2015_WO_FOX_POOLB.html',
                             RAW_GAMES_FILES + 'WC2015_WO_FOX_POOLC.html',
                             RAW_GAMES_FILES + 'WC2015_WO_FOX_POOLD.html',
                             RAW_GAMES_FILES + 'WC2015_WO_FOX_DIVONE.html',
                             RAW_GAMES_FILES + 'WC2015_WO_FOX_DIVTWO.html',
                             RAW_GAMES_FILES + 'WC2015_WO_FOX_CHAMPIONSHIP.html',
                             RAW_GAMES_FILES + 'WC2015_WO_FOX_PLATE.html']

local_files_WC_2015_W27_FX = [RAW_GAMES_FILES + 'WC2015_W27_FOX_POOLA.html',
                              RAW_GAMES_FILES + 'WC2015_W27_FOX_CHAMPIONSHIP.html']

local_files_WC_2015_MXO_FX = [RAW_GAMES_FILES + 'WC2015_MXO_FOX_POOLA.html',
                              RAW_GAMES_FILES + 'WC2015_MXO_FOX_POOLB.html',
                              RAW_GAMES_FILES + 'WC2015_MXO_FOX_POOLC.html',
                              RAW_GAMES_FILES + 'WC2015_MXO_FOX_POOLD.html',
                              RAW_GAMES_FILES + 'WC2015_MXO_FOX_POOLE.html',
                              RAW_GAMES_FILES + 'WC2015_MXO_FOX_POOLF.html',
                              RAW_GAMES_FILES + 'WC2015_MXO_FOX_DIVONE.html',
                              RAW_GAMES_FILES + 'WC2015_MXO_FOX_DIVTWO.html',
                              RAW_GAMES_FILES + 'WC2015_MXO_FOX_DIVTHREE.html',
                              RAW_GAMES_FILES + 'WC2015_MXO_FOX_CHAMPIONSHIP.html',
                              RAW_GAMES_FILES + 'WC2015_MXO_FOX_PLATE.html',
                              RAW_GAMES_FILES + 'WC2015_MXO_FOX_BRONZE.html']

local_files_WC_2015_SMX_FX = [RAW_GAMES_FILES + 'WC2015_SMX_FOX_POOLA.html',
                              RAW_GAMES_FILES + 'WC2015_SMX_FOX_PLAYOFF.html',
                              RAW_GAMES_FILES + 'WC2015_SMX_FOX_CHAMPIONSHIP.html']

local_files_NTL_2016_M_FX = [RAW_GAMES_FILES + 'NTL2016_MO_FOX_POOLA.html',
                             RAW_GAMES_FILES + 'NTL2016_MO_FOX_FINALS.html']

local_files_NTL_2016_WO_FX = [RAW_GAMES_FILES + 'NTL2016_WO_FOX_POOLA.html',
                              RAW_GAMES_FILES + 'NTL2016_WO_FOX_FINALS.html']

local_files_EUROS_2014_MO = [RAW_GAMES_FILES + 'EUROS2014_MO.html']
local_files_EUROS_2014_M40 = [RAW_GAMES_FILES + 'EUROS2014_M40.html']
local_files_EUROS_2014_WO = [RAW_GAMES_FILES + 'EUROS2014_WO.html']
local_files_EUROS_2014_W27 = [RAW_GAMES_FILES + 'EUROS2014_W27.html']
local_files_EUROS_2014_MXO = [RAW_GAMES_FILES + 'EUROS2014_MXO.html']
local_files_EUROS_2014_SMX = [RAW_GAMES_FILES + 'EUROS2014_SMX.html']
local_files_EUROS_2016_MO = [RAW_GAMES_FILES + 'euros/EUROS2016_MO.html']
local_files_EUROS_2016_WO = [RAW_GAMES_FILES + 'euros/EUROS2016_WO.html']
local_files_EUROS_2016_W27 = [RAW_GAMES_FILES + 'euros/EUROS2016_W27.html']
local_files_EUROS_2016_MXO = [RAW_GAMES_FILES + 'euros/EUROS2016_MXO.html']
local_files_EUROS_2016_SMX = [RAW_GAMES_FILES + 'euros/EUROS2016_SMX.html']


# CONSTANTS ALGORITHMS
WC2015_RE_GROUPS = '[Pool [A|B|C|D|E|F]|Division [1|2|3]'
WC2015_RE_FINALS = '[Grand Final|Bronze|Playoff ]'
EUROS2014_RE_FINALS = '[Final|Bronze Final|9th/10th/11th|Semi Final 1|Semi Final 2|5th/6th Playoff|7th/8th Playoff|Seeding Semi Final 1|Seeding Semi Final 2]'

(WC_2015_MO_GAMES_FOX, WC_2015_WO_GAMES_FOX, WC_2015_MXO_GAMES_FOX,
 WC_2015_W27_GAMES_FOX, WC_2015_M30_GAMES_FOX, WC_2015_SMX_GAMES_FOX,
 NTL_2016_MO_GAMES_FOX, NTL_2016_WO_GAMES_FOX,
 WC_2015_MO_GAMES_FIT, WC_2015_WO_GAMES_FIT, WC_2015_MXO_GAMES_FIT,
 EUROS_2014_MO, EUROS_2014_WO, EUROS_2014_MXO, EUROS_2014_W27, EUROS_2014_SMX, EUROS_2014_M40,
 EUROS_2016_MO, EUROS_2016_WO, EUROS_2016_MXO, EUROS_2016_W27, EUROS_2016_SMX) = (
    0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21)

local_fit_stats_files = {
    'EUROS_2014':
        {
            MO: {
                'england': RAW_STATS_FILES_EUROS + 'EUROS_2014_MO_england_stats.html',
                'wales': RAW_STATS_FILES_EUROS + 'EUROS_2014_MO_wales_stats.html',
                'scotland': RAW_STATS_FILES_EUROS + 'EUROS_2014_MO_scotland_stats.html',
                'ireland': RAW_STATS_FILES_EUROS + 'EUROS_2014_MO_ireland_stats.html',
                'france': RAW_STATS_FILES_EUROS + 'EUROS_2014_MO_france_stats.html',
                'luxembourg': RAW_STATS_FILES_EUROS + 'EUROS_2014_MO_luxembourg_stats.html',
                'belgium': RAW_STATS_FILES_EUROS + 'EUROS_2014_MO_belgium_stats.html',
                'hungary': RAW_STATS_FILES_EUROS + 'EUROS_2014_MO_hungary_stats.html',
                'italy': RAW_STATS_FILES_EUROS + 'EUROS_2014_MO_italy_stats.html'
            },
            WO: {
                'england': RAW_STATS_FILES_EUROS + 'EUROS_2014_WO_england_stats.html',
                'wales': RAW_STATS_FILES_EUROS + 'EUROS_2014_WO_wales_stats.html',
                'scotland': RAW_STATS_FILES_EUROS + 'EUROS_2014_WO_scotland_stats.html',
                'spain': RAW_STATS_FILES_EUROS + 'EUROS_2014_WO_spain_stats.html',
                'france': RAW_STATS_FILES_EUROS + 'EUROS_2014_WO_france_stats.html',
                'belgium': RAW_STATS_FILES_EUROS + 'EUROS_2014_WO_belgium_stats.html',
                'ireland': RAW_STATS_FILES_EUROS + 'EUROS_2014_WO_ireland_stats.html'
            },
            MXO: {
                'scotland': RAW_STATS_FILES_EUROS + 'EUROS_2014_MXO_scotland_stats.html',
                'england': RAW_STATS_FILES_EUROS + 'EUROS_2014_MXO_england_stats.html',
                'wales': RAW_STATS_FILES_EUROS + 'EUROS_2014_MXO_wales_stats.html',
                'jersey': RAW_STATS_FILES_EUROS + 'EUROS_2014_MXO_jersey_stats.html',
                'france': RAW_STATS_FILES_EUROS + 'EUROS_2014_MXO_france_stats.html',
                'netherlands': RAW_STATS_FILES_EUROS + 'EUROS_2014_MXO_netherlands_stats.html',
                'italy': RAW_STATS_FILES_EUROS + 'EUROS_2014_MXO_italy_stats.html',
                'guernsey': RAW_STATS_FILES_EUROS + 'EUROS_2014_MXO_guernsey_stats.html',
                'germany': RAW_STATS_FILES_EUROS + 'EUROS_2014_MXO_germany_stats.html',
                'switzerland': RAW_STATS_FILES_EUROS + 'EUROS_2014_MXO_switzerland_stats.html',
                'catalonia': RAW_STATS_FILES_EUROS + 'EUROS_2014_MXO_catalonia_stats.html'
            },
            W27: {
                'england': RAW_STATS_FILES_EUROS + 'EUROS_2014_W27_england_stats.html',
                'france': RAW_STATS_FILES_EUROS + 'EUROS_2014_W27_france_stats.html',
                'scotland': RAW_STATS_FILES_EUROS + 'EUROS_2014_W27_scotland_stats.html',
                'ireland': RAW_STATS_FILES_EUROS + 'EUROS_2014_W27_ireland_stats.html',
                'wales': RAW_STATS_FILES_EUROS + 'EUROS_2014_W27_wales_stats.html'
            },
            SMX: {
                'england': RAW_STATS_FILES_EUROS + 'EUROS_2014_SMX_england_stats.html',
                'scotland': RAW_STATS_FILES_EUROS + 'EUROS_2014_SMX_scotland_stats.html',
                'ireland': RAW_STATS_FILES_EUROS + 'EUROS_2014_SMX_ireland_stats.html',
                'wales': RAW_STATS_FILES_EUROS + 'EUROS_2014_SMX_wales_stats.html',
                'france': RAW_STATS_FILES_EUROS + 'EUROS_2014_SMX_france_stats.html'
            },
            M40: {
                'wales': RAW_STATS_FILES_EUROS + 'EUROS_2014_M40_wales_stats.html',
                'ireland': RAW_STATS_FILES_EUROS + 'EUROS_2014_M40_ireland_stats.html',
                'england': RAW_STATS_FILES_EUROS + 'EUROS_2014_M40_england_stats.html',
                'france': RAW_STATS_FILES_EUROS + 'EUROS_2014_M40_france_stats.html',
                'scotland': RAW_STATS_FILES_EUROS + 'EUROS_2014_M40_scotland_stats.html',
                'italy': RAW_STATS_FILES_EUROS + 'EUROS_2014_M40_italy_stats.html',
                'spain': RAW_STATS_FILES_EUROS + 'EUROS_2014_M40_spain_stats.html',
                'belgium': RAW_STATS_FILES_EUROS + 'EUROS_2014_M40_belgium_stats.html'
            }
        }
}

EUROS_2014 = 'EUROS_2014'
EUROS_2016 = 'EUROS_2016'
remote_fit_stats_files = {
    EUROS_2014:
        {
            MO: {
                'england': 'https://www.internationaltouch.org/events/euros/2014/mens-open/england/',
                'wales': 'https://www.internationaltouch.org/events/euros/2014/mens-open/wales/',
                'scotland': 'https://www.internationaltouch.org/events/euros/2014/mens-open/scotland/',
                'ireland': 'https://www.internationaltouch.org/events/euros/2014/mens-open/ireland/',
                'france': 'https://www.internationaltouch.org/events/euros/2014/mens-open/france/',
                'luxembourg': 'https://www.internationaltouch.org/events/euros/2014/mens-open/luxembourg/',
                'belgium': 'https://www.internationaltouch.org/events/euros/2014/mens-open/belgium/',
                'hungary': 'https://www.internationaltouch.org/events/euros/2014/mens-open/hungary/',
                'italy': 'https://www.internationaltouch.org/events/euros/2014/mens-open/italy/'
            },
            WO: {
                'england': 'https://www.internationaltouch.org/events/euros/2014/womens-open/england/',
                'wales': 'https://www.internationaltouch.org/events/euros/2014/womens-open/wales/',
                'scotland': 'https://www.internationaltouch.org/events/euros/2014/womens-open/scotland/',
                'spain': 'https://www.internationaltouch.org/events/euros/2014/womens-open/spain/',
                'france': 'https://www.internationaltouch.org/events/euros/2014/womens-open/france/',
                'belgium': 'https://www.internationaltouch.org/events/euros/2014/womens-open/belgium/',
                'ireland': 'https://www.internationaltouch.org/events/euros/2014/womens-open/ireland/'
            },
            MXO: {
                'scotland': 'https://www.internationaltouch.org/events/euros/2014/mixed-open/scotland/',
                'england': 'https://www.internationaltouch.org/events/euros/2014/mixed-open/england/',
                'wales': 'https://www.internationaltouch.org/events/euros/2014/mixed-open/wales/',
                'jersey': 'https://www.internationaltouch.org/events/euros/2014/mixed-open/jersey/',
                'france': 'https://www.internationaltouch.org/events/euros/2014/mixed-open/france/',
                'netherlands': 'https://www.internationaltouch.org/events/euros/2014/mixed-open/netherlands/',
                'italy': 'https://www.internationaltouch.org/events/euros/2014/mixed-open/italy/',
                'guernsey': 'https://www.internationaltouch.org/events/euros/2014/mixed-open/guernsey/',
                'germany': 'https://www.internationaltouch.org/events/euros/2014/mixed-open/germany/',
                'switzerland': 'https://www.internationaltouch.org/events/euros/2014/mixed-open/switzerland/',
                'catalonia': 'https://www.internationaltouch.org/events/euros/2014/mixed-open/catalonia/'
            },
            W27: {
                'england': 'https://www.internationaltouch.org/events/euros/2014/womens-27/england/',
                'france': 'https://www.internationaltouch.org/events/euros/2014/womens-27/france/',
                'scotland': 'https://www.internationaltouch.org/events/euros/2014/womens-27/scotland/',
                'ireland': 'https://www.internationaltouch.org/events/euros/2014/womens-27/ireland/',
                'wales': 'https://www.internationaltouch.org/events/euros/2014/womens-27/wales/'
            },
            SMX: {
                'england': 'https://www.internationaltouch.org/events/euros/2014/senior-mixed/england/',
                'scotland': 'https://www.internationaltouch.org/events/euros/2014/senior-mixed/england/',
                'ireland': 'https://www.internationaltouch.org/events/euros/2014/senior-mixed/ireland/',
                'wales': 'https://www.internationaltouch.org/events/euros/2014/senior-mixed/wales/',
                'france': 'https://www.internationaltouch.org/events/euros/2014/senior-mixed/france/'
            },
            M40: {
                'wales': 'https://www.internationaltouch.org/events/euros/2014/mens-40/wales/',
                'ireland': 'https://www.internationaltouch.org/events/euros/2014/mens-40/ireland/',
                'england': 'https://www.internationaltouch.org/events/euros/2014/mens-40/england/',
                'france': 'https://www.internationaltouch.org/events/euros/2014/mens-40/france/',
                'scotland': 'https://www.internationaltouch.org/events/euros/2014/mens-40/scotland/',
                'italy': 'https://www.internationaltouch.org/events/euros/2014/mens-40/italy/',
                'spain': 'https://www.internationaltouch.org/events/euros/2014/mens-40/spain/',
                'belgium': 'https://www.internationaltouch.org/events/euros/2014/mens-40/belgium/'
            }
        }
}
