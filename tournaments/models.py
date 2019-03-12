from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import smart_str
from django_countries.fields import CountryField


DATA_FILES = './data_files/'

MIXED_OPEN = _('Mixed')
MEN_OPEN = _('Men')
WOMEN_OPEN = _('Women')

SENIOR_MIX = _('Senior Mix Open')
MIX_40 = _('Mixed 40')

MEN_30 = _('Men 30')
MEN_40 = _('Men 40')
MEN_45 = _('Men 45')
SENIOR_WOMEN = _('Senior Women Open')
WOMEN_27 = _('Women 27')
WOMEN_40 = _('Women 40')

MXO = 'MXO'
MO = 'MO'
WO = 'WO'
SMX = 'SMX'
W27 = 'W27'
M30 = 'M30'
M40 = 'M40'
M45 = 'M45'
W40 = 'W40'


PADEL_DIVISION_CHOICES_ALL = (
    ('ALL', _('ALL')), ('MO', _('Men')), ('WO', _('Women')), ('XO', _('Mixed')),
    ('M45', _('Men 45')), ('W40', _('Women 40')), ('X40', _('Mixed 40'))
)

PADEL_DIVISION_CHOICES = (
    ('MO', _('Men')), ('WO', _('Women')), ('XO', _('Mixed')),
    ('M45', _('Men 45')), ('W40', _('Women 40')), ('X40', _('Mixed 40'))
)

TOUCH_DIVISION_CHOICES = (
    (MXO, MIXED_OPEN),
    (MO, MEN_OPEN),
    (WO, WOMEN_OPEN),
    (SMX, SENIOR_MIX),
    (M30, MEN_30),
    (M40, MEN_40),
    (M45, MEN_45),
    (W27, WOMEN_27),
    (W40, WOMEN_40)
)

SERIE_GERMANY = (('GPS-100', 'GPS-100'), ('GPS-250', 'GPS-250'), ('GPS-500', 'GPS-500'), ('GPS-1000', 'GPS-1000'),
                 ('GPS-1200', 'GPS-1200'), ('GPS-WOMEN', 'GPS-WOMEN'))


def get_player_gender(division):
    if division in [WO, W27, W40]:
        result = Person.FEMALE
    elif division in [MO, M30, M40, M45]:
        result = Person.MALE
    elif division in [MXO, SMX]:
        result = Person.UNKNOWN
    else:
        raise Exception("Division %s is not supported." % division)
    return result


def club_directory_path(instance, filename):
    return 'club_media/' + normalize(no_german_chars('{0}-{1}'.format(instance.name, filename)))


class Person(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    UNKNOWN = 'U'
    GENDER_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (UNKNOWN, None)
    )

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    born = models.DateField(null=True, blank=True)
    country = CountryField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, default=UNKNOWN)

    class Meta:
        ordering = ['gender', 'last_name', 'first_name']

    def __str__(self):
        return '{0} {1} - {2}'.format(smart_str(self.first_name), smart_str(self.last_name), self.gender)

    def get_full_name(self):
        """Returns the person's full name."""
        return '{0} {1}'.format(smart_str(self.first_name), smart_str(self.last_name))

    def get_full_name_reverse(self):
        """Returns the person's full name."""
        return '{0}, {1}'.format(smart_str(self.last_name), smart_str(self.first_name))

    def compare_name(self, other):
        """Returns True if both persons have the same full name otherwise False."""
        return self.get_full_name() == other.get_full_name()

    def __lt__(self, other):
        if self.gender != other.gender:
            if self.gender == self.FEMALE or other.gender == self.UNKNOWN:
                return True
            else:
                return False
        else:
            return self.last_name <= other.last_name

    def get_png_flag(self):
        return 'images/flags/16/Germany.png'


class Team(models.Model):
    name = models.CharField(max_length=40)
    players = models.ManyToManyField(Person, through='Player')
    division = models.CharField(max_length=3, choices=TOUCH_DIVISION_CHOICES)

    def __str__(self):
        return self.name


class Club(models.Model):
    name = models.CharField(max_length=50)
    city = models.CharField(max_length=30)
    province = models.CharField(max_length=30)
    postcode = models.PositiveIntegerField(validators=[MinValueValidator(99), MaxValueValidator(1000000)])
    email = models.EmailField()
    phone = models.CharField(max_length=24)
    address = models.CharField(max_length=120, blank=True)
    indoor_courts = models.PositiveIntegerField()
    outdoor_courts = models.PositiveIntegerField()
    logo = models.ImageField(upload_to=club_directory_path, default='default.jpg')
    cover_photo = models.ImageField(upload_to=club_directory_path, default='pista.jpg')

    def __str__(self):
        return self.name


class Tournament(models.Model):
    TOURNAMENT_CHOICES = (("PADEL", "PADEL"), ("TOUCH", "TOUCH"))
    type = models.CharField(max_length=10, choices=TOURNAMENT_CHOICES, default="PADEL")
    name = models.CharField(max_length=50)
    country = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    address = models.CharField(max_length=100, null=True, blank=True, default=None)
    date = models.DateField(null=True, blank=True)
    teams = models.ManyToManyField(Team, blank=True)
    division = models.CharField(max_length=3, choices=TOUCH_DIVISION_CHOICES, null=True, blank=True)
    padel_serie = models.CharField(choices=SERIE_GERMANY, max_length=20, default='GPS-500', null=True, blank=True)
    signup = models.BooleanField(default=False)
    finished = models.BooleanField(default=False)
    club = models.ForeignKey(Club, on_delete=models.SET_NULL, blank=True, null=True, default=None)

    class Meta:
        ordering = ['name']

    def __str__(self):
        # padel
        if self.padel_serie and self.city and self.division and self.date:
            return "  /  ".join([str(self.date), str(self.padel_serie), str(self.city), str(self.division)])
        # touch
        if self.country and self.city:
            result = '{0} - {1} ({2}, {3})'.format(
                self.division, self.name, smart_str(self.city), smart_str(self.country))
        elif self.country:
            result = '{0} - {1} ({2})'.format(self.division, self.name, smart_str(self.country))
        elif self.city:
            result = '{0} - {1} ({2})'.format(self.division, self.name, smart_str(self.city))
        else:
            result = '{0} - {1}'.format(self.division, self.name)
        return result

    def __lt__(self, other):
        if self.name >= other.name:
            result = False
        else:
            result = True
        return result

    def turnierliste_key(self):
        return " ".join([str(self.padel_serie), str(self.city), str(self.date)])

    @property
    def serie_url(self):
        if self.padel_serie == 'GPS-100':
            return 'images/kategorien/gps100.jpg'
        elif self.padel_serie == 'GPS-250':
            return 'images/kategorien/gps250.jpg'
        elif self.padel_serie == 'GPS-500':
            return 'images/kategorien/gps500.jpg'
        elif self.padel_serie == 'GPS-1000':
            return 'images/kategorien/gps1000.jpg'
        elif self.padel_serie == 'GPS-1200':
            return 'images/kategorien/gps1200.jpg'
        elif self.padel_serie == 'GPS-WOMEN':
            return 'images/kategorien/w-gps.jpg'
        else:
            raise TypeError("The serie is not supported.")

    def get_division_name(self):
        for x in TOUCH_DIVISION_CHOICES:
            if self.division == x[0]:
                if 'MO' == x[0]:
                    return MEN_OPEN
                elif 'WO' == x[0]:
                    return WOMEN_OPEN
                elif 'MXO' == x[0]:
                    return MIXED_OPEN
                elif 'M30' == x[0]:
                    return MEN_30
                elif 'M40' == x[0]:
                    return MEN_40
                elif 'SMX' == x[0]:
                    return SENIOR_MIX
                elif 'W27' == x[0]:
                    return WOMEN_27

        assert "A name for the division: %s could not be found." % self.division


class Player(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, blank=True)
    number = models.PositiveSmallIntegerField(null=True, blank=True)
    tournaments_played = models.ManyToManyField(Tournament, blank=True)

    class Meta:
        ordering = ["person"]

    def __str__(self):
        return '{:s},  {:s} {:s}'.format(str(self.team), str(self.number), str(self.person))


class GameRound(models.Model):
    FINAL = 'KO1'
    SEMI = 'KO2'
    QUARTER = 'KO4'
    EIGHTH = 'KO8'
    SIXTEENTH = 'KO16'
    THIRD_POSITION = 'POS3'
    FIFTH_POSITION = 'POS5'
    SIXTH_POSITION = 'POS6'
    SEVENTH_POSITION = 'POS7'
    EIGHTH_POSITION = 'POS8'
    NINTH_POSITION = 'POS9'
    TENTH_POSITION = 'POS10'
    ELEVENTH_POSITION = 'POS11'
    TWELFTH_POSITION = 'POS12'
    THIRTEENTH_POSITION = 'POS13'
    FOURTEENTH_POSITION = 'POS14'
    FIFTEENTH_POSITION = 'POS15'
    SIXTEENTH_POSITION = 'POS16'
    EIGHTEENTH_POSITION = 'POS18'
    TWENTIETH_POSITION = 'POS20'
    DIVISION = 'Division'
    POOL_A = 'PoolA'
    POOL_B = 'PoolB'
    POOL_C = 'PoolC'
    POOL_D = 'PoolD'
    POOL_E = 'PoolE'
    POOL_F = 'PoolF'
    LIGA = 'Liga'

    pools = [POOL_A, POOL_B, POOL_C, POOL_D, POOL_E, POOL_F]

    ordered_rounds = [FINAL, THIRD_POSITION, SEMI, FIFTH_POSITION, QUARTER, SIXTH_POSITION,
                      SEVENTH_POSITION, EIGHTH_POSITION, EIGHTH, NINTH_POSITION, TENTH_POSITION,
                      ELEVENTH_POSITION, TWELFTH_POSITION, SIXTEENTH, THIRTEENTH_POSITION, FOURTEENTH_POSITION,
                      FIFTEENTH_POSITION, SIXTEENTH_POSITION, EIGHTEENTH_POSITION, TWENTIETH_POSITION]

    GAME_ROUND_CHOICES = (
        (FINAL, FINAL),
        (SEMI, SEMI),
        (QUARTER, QUARTER),
        (EIGHTH, EIGHTH),
        (SIXTEENTH, SIXTEENTH),
        (THIRD_POSITION, THIRD_POSITION),
        (FIFTH_POSITION, FIFTH_POSITION),
        (SIXTH_POSITION, SIXTH_POSITION),
        (SEVENTH_POSITION, SEVENTH_POSITION),
        (EIGHTH_POSITION, EIGHTH_POSITION),
        (NINTH_POSITION, NINTH_POSITION),
        (TENTH_POSITION, TENTH_POSITION),
        (ELEVENTH_POSITION, ELEVENTH_POSITION),
        (TWELFTH_POSITION, TWELFTH_POSITION),
        (THIRTEENTH_POSITION, THIRTEENTH_POSITION),
        (FIFTEENTH_POSITION, FIFTEENTH_POSITION),
        (SIXTEENTH_POSITION, SIXTEENTH_POSITION),
        (EIGHTEENTH_POSITION, EIGHTEENTH_POSITION),
        (TWENTIETH_POSITION, TWENTIETH_POSITION),
        (DIVISION, DIVISION),
        (POOL_A, POOL_A),
        (POOL_B, POOL_B),
        (POOL_C, POOL_C),
        (POOL_D, POOL_D),
        (POOL_E, POOL_E),
        (POOL_F, POOL_F),
        (LIGA, LIGA),
    )

    GOLD = 'Gold'
    SILVER = 'Silver'
    BRONZE = 'Bronze'
    WOOD = 'Wood'

    CATEGORY_ROUND_CHOICES = (
        (GOLD, GOLD),
        (SILVER, SILVER),
        (BRONZE, BRONZE),
        (WOOD, WOOD),
    )

    round = models.CharField(default=POOL_A, max_length=32, null=False, blank=False, choices=GAME_ROUND_CHOICES)
    number_teams = models.PositiveIntegerField(default=2, validators=[MinValueValidator(0), MaxValueValidator(20)])
    category = models.CharField(default=GOLD, max_length=6, null=False, blank=False, choices=CATEGORY_ROUND_CHOICES)

    def __str__(self):
        return '{:s} {:s} {:s}'.format(str(self.round), str(self.number_teams), str(self.category))

    def is_pool(self):
        return self.round == self.POOL_A or self.round == self.POOL_B or self.round == self.POOL_C or \
               self.round == self.POOL_D or self.round == self.POOL_E or self.round == self.POOL_F

    def __lt__(self, other):
        #        print('self = %s, other = %s' %(self, other))
        if self.category == other.category:
            if self.round == other.round:
                result = self.number_teams.__lt__(other.number_teams)
            else:
                if self.round == self.THIRD_POSITION:
                    result = False
                elif other.round == self.THIRD_POSITION:
                    result = True
                elif self.round == self.FINAL:
                    result = False
                elif other.round == self.FINAL:
                    result = True
                elif self.round == self.SEMI:
                    result = False
                elif other.round == self.SEMI:
                    result = True
                elif self.round == self.FIFTH_POSITION:
                    result = False
                elif other.round == self.FIFTH_POSITION:
                    result = True
                elif self.round == self.SIXTH_POSITION:
                    result = False
                elif other.round == self.SIXTH_POSITION:
                    result = True
                elif self.round == self.SEVENTH_POSITION:
                    result = False
                elif other.round == self.SEVENTH_POSITION:
                    result = True
                elif self.round == self.QUARTER:
                    result = False
                elif other.round == self.QUARTER:
                    result = True
                elif self.round == self.EIGHTH:
                    result = False
                elif other.round == self.EIGHTH:
                    result = True
                elif self.round == self.EIGHTH_POSITION:
                    result = False
                elif other.round == self.EIGHTH_POSITION:
                    result = True
                elif self.round == self.NINTH_POSITION:
                    result = False
                elif other.round == self.NINTH_POSITION:
                    result = True
                elif self.round == self.TENTH_POSITION:
                    result = False
                elif other.round == self.TENTH_POSITION:
                    result = True
                elif self.round == self.ELEVENTH_POSITION:
                    result = False
                elif other.round == self.ELEVENTH_POSITION:
                    result = True
                elif self.round == self.TWELFTH_POSITION:
                    result = False
                elif other.round == self.TWELFTH_POSITION:
                    result = True
                elif self.round == self.THIRTEENTH_POSITION:
                    result = False
                elif other.round == self.THIRTEENTH_POSITION:
                    result = True
                elif self.round == self.FIFTEENTH_POSITION:
                    result = False
                elif other.round == self.FIFTEENTH_POSITION:
                    result = True
                elif self.round == self.SIXTEENTH_POSITION:
                    result = False
                elif other.round == self.SIXTEENTH_POSITION:
                    result = True
                elif self.round == self.SIXTEENTH:
                    result = False
                elif other.round == self.SIXTEENTH:
                    result = True
                elif self.round == self.EIGHTEENTH_POSITION:
                    result = False
                elif other.round == self.EIGHTEENTH_POSITION:
                    result = True
                elif self.round == self.TWENTIETH_POSITION:
                    result = False
                elif other.round == self.TWENTIETH_POSITION:
                    result = True
                elif self.round == self.DIVISION:
                    result = False
                elif other.round == self.DIVISION:
                    result = True
                elif self.round in {self.POOL_A, self.POOL_B, self.POOL_C, self.POOL_D, self.POOL_E, self.POOL_F}:
                    result = False
                elif other.round in {self.POOL_A, self.POOL_B, self.POOL_C, self.POOL_D, self.POOL_E, self.POOL_F}:
                    result = True
                else:
                    raise Exception('Problem comparing values: %s and  %s' % (self.round, other.round))
        else:
            if self.category == self.GOLD:
                result = False
            elif other.category == self.GOLD:
                result = True
            elif self.category == self.SILVER:
                result = False
            elif other.category == self.SILVER:
                result = True
            elif self.category == self.BRONZE:
                result = False
            elif other.category == self.BRONZE:
                result = True
            elif self.category == self.WOOD:
                result = False
            else:
                raise Exception('Problem comparing values: %s and  %s' % (self.category, other.category))
        return result

    def __cmp__(self, other):
        #        print('self = %s, other = %s' %(self, other))
        if self.category == other.category:
            if self.round == other.round:
                result = self.number_teams.__cmp__(other.number_teams)
            else:
                if self.round == self.THIRD_POSITION:
                    result = 1
                elif other.round == self.THIRD_POSITION:
                    result = -1
                elif self.round == self.FINAL:
                    result = 1
                elif other.round == self.FINAL:
                    result = -1
                elif self.round == self.SEMI:
                    result = 1
                elif other.round == self.SEMI:
                    result = -1
                elif self.round == self.FIFTH_POSITION:
                    result = 1
                elif other.round == self.FIFTH_POSITION:
                    result = -1
                elif self.round == self.SIXTH_POSITION:
                    result = 1
                elif other.round == self.SIXTH_POSITION:
                    result = -1
                elif self.round == self.SEVENTH_POSITION:
                    result = 1
                elif other.round == self.SEVENTH_POSITION:
                    result = -1
                elif self.round == self.QUARTER:
                    result = 1
                elif other.round == self.QUARTER:
                    result = -1
                elif self.round == self.EIGHTH:
                    result = 1
                elif other.round == self.EIGHTH:
                    result = -1
                elif self.round == self.NINTH_POSITION:
                    result = 1
                elif other.round == self.NINTH_POSITION:
                    result = -1
                elif self.round == self.TENTH_POSITION:
                    result = 1
                elif other.round == self.TENTH_POSITION:
                    result = -1
                elif self.round == self.ELEVENTH_POSITION:
                    result = 1
                elif other.round == self.ELEVENTH_POSITION:
                    result = -1
                elif self.round == self.TWELFTH_POSITION:
                    result = 1
                elif other.round == self.TWELFTH_POSITION:
                    result = -1
                elif self.round == self.THIRTEENTH_POSITION:
                    result = 1
                elif other.round == self.THIRTEENTH_POSITION:
                    result = -1
                elif self.round == self.FIFTEENTH_POSITION:
                    result = 1
                elif other.round == self.FIFTEENTH_POSITION:
                    result = -1
                elif self.round == self.SIXTEENTH_POSITION:
                    result = 1
                elif other.round == self.SIXTEENTH_POSITION:
                    result = -1
                elif self.round == self.SIXTEENTH:
                    result = 1
                elif other.round == self.SIXTEENTH:
                    result = -1
                elif self.round == self.EIGHTEENTH_POSITION:
                    result = 1
                elif other.round == self.EIGHTEENTH_POSITION:
                    result = -1
                elif self.round == self.TWENTIETH_POSITION:
                    result = 1
                elif other.round == self.TWENTIETH_POSITION:
                    result = -1
                else:
                    raise Exception('Problem comparing values: %s and  %s' % (self.round, other.round))
        else:
            if self.category == self.GOLD:
                result = 1
            elif other.category == self.GOLD:
                result = -1
            elif self.category == self.SILVER:
                result = 1
            elif other.category == self.SILVER:
                result = -1
            elif self.category == self.BRONZE:
                result = 1
            elif other.category == self.BRONZE:
                result = -1
            elif self.category == self.WOOD:
                result = 1
            else:
                raise Exception('Problem comparing values: %s and  %s' % (self.category, other.category))
        return result


class GameField(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):  # Python 3: def __str__(self):
        return '{}'.format(self.name)


class PadelResult(models.Model):
    """
    Result of a game of Padel

    It supports so far until 5 sets. Each set is a smallInteger. If a set is null then there is no result for such set.
    When a set is null then bigger set must be also null.
    """
    local1 = models.SmallIntegerField(null=True, blank=True)
    local2 = models.SmallIntegerField(null=True, blank=True)
    local3 = models.SmallIntegerField(null=True, blank=True)
    local4 = models.SmallIntegerField(null=True, blank=True)
    local5 = models.SmallIntegerField(null=True, blank=True)

    visitor1 = models.SmallIntegerField(null=True, blank=True)
    visitor2 = models.SmallIntegerField(null=True, blank=True)
    visitor3 = models.SmallIntegerField(null=True, blank=True)
    visitor4 = models.SmallIntegerField(null=True, blank=True)
    visitor5 = models.SmallIntegerField(null=True, blank=True)

    @classmethod
    def create(cls, scores):
        while scores[len(scores)-1] == '':
            del(scores[-1])
        result = cls(local1=scores[0], visitor1=scores[1])
        try:
            result.local2 = scores[2]
            result.visitor2 = scores[3]
            result.local3 = scores[4]
            result.visitor3 = scores[5]
            result.local4 = scores[6]
            result.visitor4 = scores[7]
            result.local5 = scores[8]
            result.visitor5 = scores[9]
        except IndexError:
            pass
        return result

    def _get_local_scores(self):
        return self._get_scores_lists()[0]

    def _get_visitor_scores(self):
        return self._get_scores_lists()[1]
    
    def _get_scores_lists(self):
        local = list()
        visitor = list()
        scores = [self.local1, self.visitor1, self.local2, self.visitor2, self.local3, self.visitor3,
                  self.local4, self.visitor4, self.local5, self.visitor5]

        for i in range(len(scores)):
            if scores[i] is not None:
                if i % 2 == 0:
                    local.append(scores[i])                
                else:
                    visitor.append(scores[i])
            else:
                break

        return local, visitor

    def get_result_pairs(self):
        result = list()
        for index in range(len(self.local_scores)):
            x = self.local_scores[index]
            y = self.visitor_scores[index]
            result.append(str(x) + '-' + str(y))
        return result

    local_scores = property(_get_local_scores)
    visitor_scores = property(_get_visitor_scores)


class Game(models.Model):
    field = models.ForeignKey(GameField, on_delete=models.SET_NULL, blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    local = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="local", null=True, blank=True)
    visitor = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="visitor", null=True, blank=True)
    local_score = models.SmallIntegerField(null=True, blank=True)
    visitor_score = models.SmallIntegerField(null=True, blank=True)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    phase = models.ForeignKey(GameRound, on_delete=models.CASCADE)
    result_padel = models.ForeignKey(PadelResult, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return '{} - {} - {} {} - {} {}'.format(
                self.tournament, self.phase, self.local, self.local_score, self.visitor_score, self.visitor)

    def __lt__(self, other):
        return self.phase.__lt__(other.phase)

    def __cmp__(self, other):
        return self.phase.__cmp__(other.phase)


class PlayerStadistic(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    points = models.PositiveSmallIntegerField(null=True, blank=True, default=0)
    mvp = models.PositiveSmallIntegerField(null=True, blank=True, default=0)
    played = models.PositiveSmallIntegerField(null=True, blank=True, default=0)
    game = models.ForeignKey(Game, on_delete=models.SET_NULL, null=True)
    tournament = models.ForeignKey(Tournament, on_delete=models.SET_NULL, null=True)

    def clean(self):
        if not self.game or not self.tournament:
            raise ValidationError(_('PlayerStatistic must be related either to a game or to a tournament.'))

    def is_game_stat(self):
        return True if self.game else False

    def is_tournament_stat(self):
        return not self.is_game_stat()

    def __str__(self):
        if self.is_game_stat():
            return '{} - {} - touchdowns: {}'.format(self.game, self.player, self.points)
        else:
            return '{} - {} - touchdowns: {} - played: {} - mvp: {}'.format(
                    self.tournament, self.player, self.points, self.played, self.mvp)


class PadelRanking(models.Model):
    OFFICIAL = 'Official'
    AUDI_PLAYDAYS = 'Audi PlayDays'
    CIRCUIT = ((OFFICIAL, OFFICIAL), (AUDI_PLAYDAYS, AUDI_PLAYDAYS))

    date = models.DateField()
    points = models.PositiveIntegerField(default=0, null=False)
    variation = models.SmallIntegerField(default=None, null=True, blank=True)
    division = models.CharField(max_length=3, choices=TOUCH_DIVISION_CHOICES)
    country = CountryField()
    circuit = models.CharField(max_length=30, default="oficial", choices=CIRCUIT)
    person = models.ForeignKey(Person, related_name="person", on_delete=models.DO_NOTHING,
                               null=True, blank=True, default=None)


def get_padel_ranking(date=None, division=None):
    if division is None:
        division = MO
    if date is None:
        date = last_monday()
    return PadelRanking.objects.filter(division=division).filter(date=date).order_by('-points')


def get_tournament_games(tournament):
    return Game.objects.filter(tournament=tournament)


def get_padel_tournament_teams(tournament):
    teams = Team.objects.filter(tournament__id=tournament.id)
    for team in teams:
        players = team.players.all()
        team.player_a = players[0]
        # case bye player:
        if len(players) == 1 and team.player_a.first_name.lower() == "bye":
            team.player_b = players[0]
        else:
            team.player_b = players[1]
    return teams


def get_clubs():
    return Club.objects.all()


def get_padel_tournament(id):
    return Tournament.objects.get(pk=id)


def get_padel_tournaments(year=None, division=None):
    if year == 'ALL':
        year = None
    if division == 'ALL':
        division = None

    if year and division is None:
        return Tournament.objects.order_by('-date', 'city').filter(date__year=year)
    elif year is None and division:
        return Tournament.objects.order_by('-date', 'city').filter(division=division)
    elif year and division:
        return Tournament.objects.order_by('-date', 'city').filter(date__year=year).filter(division=division)
    else:
        return Tournament.objects.order_by('-date', 'city')


def translate_division(division):
    translations = {'MO': _('Men'), 'WO': _('Women'), 'XO': _('Mixed'), 'MXO': _('Mixed'),
                    'M45': _('Men 45'), 'W40': _('Women 40'), 'X40': _('Mixed 40'), 'SMX': _('Senior Mixed')}
    return translations[division]


def get_similar_tournaments(t_id):
    result = dict()
    tournament = get_padel_tournament(t_id)
    if tournament.date:
        similars = Tournament.objects.filter(date=tournament.date, city=tournament.city)
        for t in similars:
            if t.id != tournament.id:
                result[str(t.padel_serie) + ' ' + str(translate_division(t.division))] = t.id
    print(result)
    return result


def normalize(filename):
    return "".join([c for c in filename if c.isalpha() or c.isdigit() or c == ' ']).rstrip()


def no_german_chars(string):
    chars = {'ö': 'oe', 'ä': 'ae', 'ü': 'ue', 'ß': 'ss'}
    for c in chars:
        string = string.replace(c, chars[c])
    return string


def last_monday():
    from datetime import datetime, timedelta
    d = datetime.now().date()
    d -= timedelta(days=d.weekday())
    return d


def total_tournaments():
    return Tournament.objects.all().count()


def total_clubs():
    return Club.objects.all().count()


def total_persons():
    return Person.objects.all().count()


def total_rankings():
    return PadelRanking.objects.values('division').distinct().count()


def total_courts():
    from django.db.models import Sum, F
    return Club.objects.all().aggregate(total=Sum(F('indoor_courts') + F('outdoor_courts')))['total']
