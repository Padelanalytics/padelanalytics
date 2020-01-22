# Coppyright (c) 2015 Francisco Javier Revilla Linares to present.
# All rights reserved.
from collections import OrderedDict
from datetime import date, datetime, timedelta

from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
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

O = 'O'
XO = 'XO'
MO = 'MO'
WO = 'WO'
SMX = 'SMX'
X40 = 'X40'
W27 = 'W27'
M30 = 'M30'
M35 = 'M35'
M40 = 'M40'
M45 = 'M45'
W35 = 'W35'
W40 = 'W40'
X40 = 'X40'
order_divisions = [MO, WO, O, XO, M30, W35, M35, M40, W40, X40, M45]

FEDERATION_CHOICES = (("GERMANY", "Germany"), ("NETHERLANDS", "Netherlands"), ("THAILAND", "Thailand"))

PADEL_DIVISION_CHOICES_ALL = (
    ('ALL', _('ALL')), ('MO', _('Men')), ('WO', _('Women')), ('XO', _('Mixed')), ('O', _('Open')),
    ('M40', _('Men 40')), ('M45', _('Men 45')),
    ('W40', _('Women 40')), ('X40', _('Mixed 40'))
)

PADEL_DIVISION_CHOICES = (
    ('MO', _('Men')), ('WO', _('Women')), ('XO', _('Mixed')),
    ('M40', _('Men 40')), ('M45', _('Men 45')),
    ('W40', _('Women 40')), ('X40', _('Mixed 40'))
)

TOUCH_DIVISION_CHOICES = (
    (XO, MIXED_OPEN),
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
                 ('GPS-1200', 'GPS-1200'), ('GPS-2000', 'GPS-2000'), ('GPS-WOMEN', 'GPS-WOMEN'))

SERIES_NETHERLANDS = (('NK', 'NK'),
('NPB-250-HK', 'NPB-250-HK'), ('NPB-250-1K', 'NPB-250-1K'), ('NPB-250-2K', 'NPB-250-2K'), ('NPB-250-3K', 'NPB-250-3K'),
('NPB-100-HK', 'NPB-100-HK'), ('NPB-100-1K', 'NPB-100-1K'), ('NPB-100-2K', 'NPB-100-2K'), ('NPB-100-3K', 'NPB-100-3K'),
('NPB-250-Mix', 'NPB-250-Mix'), ('NPB-100-Mix', 'NPB-100-Mix'))

SERIES_THAILAND = (('TH-A', 'TH-A'), ('TH-B', 'TH-B'))

SERIES_FIP = (('FIP-PROMOTION', 'FIP-PROMOTION'), ('FIP-RISE', 'FIP-RISE'), ('FIP-STAR', 'FIP-STAR'),
('FIP-100', 'FIP-100'), ('FIP-125', 'FIP-125'), ('FIP-250', 'FIP-250') , ('FIP-500', 'FIP-500'), ('FIP-1000', 'FIP-1000'),
('WPT-CHALLENGER', 'WPT-CHALLENGER'), ('WPT-OPEN', 'WPT-OPEN'), ('WPT-MASTER', 'WPT-MASTER'), ('WPT-MASTERFINAL', 'WPT-MASTERFINAL'))


def get_last_ranking_date():
    return date(2019, 12, 30)


def get_player_gender(division):
    if division in [WO, W27, W35, W40]:
        result = Person.FEMALE
    elif division in [MO, M30, M35, M40, M45]:
        result = Person.MALE
    elif division in [O, XO, SMX, X40]:
        result = Person.UNKNOWN
    else:
        raise Exception("Division %s is not supported." % division)
    return result


def club_directory_path(instance, filename):
    return 'club_media/' + normalize(no_german_chars('{0}-{1}'.format(instance.name, filename)))


class Club(models.Model):
    federation = models.CharField(max_length=25, choices=FEDERATION_CHOICES, default="GERMANY")
    name = models.CharField(max_length=50)
    city = models.CharField(max_length=30)
    province = models.CharField(max_length=30)
    postcode = models.CharField(max_length=10)
    email = models.EmailField()
    website = models.URLField(null=True, blank=True)
    phone = models.CharField(max_length=24)
    address = models.CharField(max_length=120, blank=True)
    indoor_courts = models.PositiveIntegerField()
    outdoor_courts = models.PositiveIntegerField()
    logo = models.ImageField(upload_to=club_directory_path, default='club_media/_logo.png')
    cover_photo = models.ImageField(upload_to=club_directory_path, default='club_media/pista.jpg')
    new = models.BooleanField(default=False)
    old = models.BooleanField(default=False)

    @property
    def website_short(self):
        return self.website.replace('http://', '').replace('https://', '')

    def __str__(self):
        return self.name


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
    club = models.ForeignKey(Club, on_delete=models.SET_NULL, null=True, blank=True, default=None)

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


class Tournament(models.Model):
    TOURNAMENT_CHOICES = (("PADEL", "PADEL"), ("TOUCH", "TOUCH"))
    federation = models.CharField(max_length=25, choices=FEDERATION_CHOICES, default="GERMANY")
    type = models.CharField(max_length=10, choices=TOURNAMENT_CHOICES, default="PADEL")
    name = models.CharField(max_length=50)
    country = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    address = models.CharField(max_length=100, null=True, blank=True, default=None)
    date = models.DateField(null=True, blank=True)
    teams = models.ManyToManyField(Team, blank=True)
    division = models.CharField(max_length=3, choices=TOUCH_DIVISION_CHOICES, null=True, blank=True)
    padel_serie = models.CharField(
        choices=SERIE_GERMANY + SERIES_NETHERLANDS + SERIES_FIP + SERIES_THAILAND,
        max_length=20, default='GPS-500', null=True, blank=True)
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
        # Germany
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
        elif self.padel_serie == 'GPS-2000':
            return 'images/kategorien/gps2000.jpg'
        elif self.padel_serie == 'GPS-WOMEN':
            return 'images/kategorien/w-gps.jpg'
        elif self.padel_serie is None:
            return 'images/kategorien/w-gps.jpg'

        # Netherlands
        elif self.padel_serie == 'NK':
            return 'images/kategorien/NK.png'
        elif self.padel_serie == 'NPB-250-HK':
            return 'images/kategorien/NPB-250-HK.png'
        elif self.padel_serie == 'NPB-250-1K':
            return 'images/kategorien/NPB-250-1K.png'
        elif self.padel_serie == 'NPB-250-2K':
            return 'images/kategorien/NPB-250-2K.png'
        elif self.padel_serie == 'NPB-250-3K':
            return 'images/kategorien/NPB-250-3K.png'
        elif self.padel_serie == 'NPB-100-HK':
            return 'images/kategorien/NPB-100-HK.png'
        elif self.padel_serie == 'NPB-100-1K':
            return 'images/kategorien/NPB-100-1K.png'
        elif self.padel_serie == 'NPB-100-2K':
            return 'images/kategorien/NPB-100-2K.png'
        elif self.padel_serie == 'NPB-100-3K':
            return 'images/kategorien/NPB-100-3K.png'
        elif self.padel_serie == 'NPB-100-Mix':
            return 'images/kategorien/NPB-100-Mix.png'
        elif self.padel_serie == 'NPB-250-Mix':
            return 'images/kategorien/NPB-250-Mix.png'

        # Thailand
        elif self.padel_serie == 'TH-A':
            return 'images/kategorien/TH-A.png'
        elif self.padel_serie == 'TH-B':
            return 'images/kategorien/TH-B.png'

        # FIP
        elif self.padel_serie == 'FIP-PROMOTION':
            return 'images/kategorien/FIP-PROMOTION.png'
        elif self.padel_serie == 'FIP-RISE':
            return 'images/kategorien/FIP-RISE.png'
        elif self.padel_serie == 'FIP-STAR':
            return 'images/kategorien/FIP-STAR.png'
        elif self.padel_serie == 'FIP-100':
            return 'images/kategorien/FIP-100.png'
        elif self.padel_serie == 'FIP-125':
            return 'images/kategorien/FIP-125.png'
        elif self.padel_serie == 'FIP-250':
            return 'images/kategorien/FIP-250.png'
        elif self.padel_serie == 'FIP-500':
            return 'images/kategorien/FIP-500.png'
        elif self.padel_serie == 'FIP-1000':
            return 'images/kategorien/FIP-1000.png'
        elif self.padel_serie == 'WPT-CHALLENGER':
            return 'images/kategorien/WPT-CHALLENGER.png'
        elif self.padel_serie == 'WPT-OPEN':
            return 'images/kategorien/WPT-OPEN.png'
        elif self.padel_serie == 'WPT-MASTER':
            return 'images/kategorien/WPT_MASTER.png'
        elif self.padel_serie == 'WPT-MASTERFINAL':
            return 'images/kategorien/WPT_MASTERFINAL.png'
        else:
            raise TypeError("The serie: " + self.padel_serie + " is not supported.")

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
    POOL_Z = 'PoolZ'
    LIGA = 'Liga'

    pools = [POOL_A, POOL_B, POOL_C, POOL_D, POOL_E, POOL_F, POOL_Z]

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
        (POOL_Z, POOL_Z),
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
               self.round == self.POOL_D or self.round == self.POOL_E or self.round == self.POOL_F or \
               self.round == self.POOL_Z

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
                elif self.round == self.POOL_Z:
                    result = False
                elif other.round == self.POOL_Z:
                    result = True
                elif self.round == self.POOL_F:
                    result = False
                elif other.round == self.POOL_F:
                    result = True
                elif self.round == self.POOL_E:
                    result = False
                elif other.round == self.POOL_E:
                    result = True
                elif self.round == self.POOL_D:
                    result = False
                elif other.round == self.POOL_D:
                    result = True
                elif self.round == self.POOL_C:
                    result = False
                elif other.round == self.POOL_C:
                    result = True
                elif self.round == self.POOL_B:
                    result = False
                elif other.round == self.POOL_B:
                    result = True
                elif self.round == self.POOL_A:
                    result = False
                elif other.round == self.POOL_A:
                    result = True
                elif self.round in {self.POOL_A, self.POOL_B, self.POOL_C, self.POOL_D, self.POOL_E, self.POOL_F, self.POOL_Z}:
                    result = False
                elif other.round in {self.POOL_A, self.POOL_B, self.POOL_C, self.POOL_D, self.POOL_E, self.POOL_F, self.POOL_Z}:
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

    winner = models.SmallIntegerField(default=0)

    @classmethod
    def create(cls, scores):
        while scores[len(scores)-1] == '':
            del(scores[-1])
        scores = [int(s) for s in scores]
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

        # calculate the winner player (1 = local, 2 = visitor, 0 = draw)
        sets = [0, 0]
        local_scores = scores[0::2]
        visitor_scores = scores[1::2]
        for index in range(len(local_scores)):
            if local_scores[index] > visitor_scores[index]:
                sets[0] += 1
            elif local_scores[index] < visitor_scores[index]:
                sets[1] += 1

        if sets[0] > sets[1]:
            result.winner = 1
        elif sets[0] < sets[1]:
            result.winner = 2
        else:
            result.winner = 0

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

    def get_local_games_diff(self):
        diff = 0
        for i in self._get_local_scores():
            diff += i
        for i in self._get_visitor_scores():
            diff -= i
        return diff

    def get_visitor_games_diff(self):
        return -1 * self.get_local_games_diff()

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
    plus = models.PositiveSmallIntegerField(default=None, null=True, blank=True)
    minus = models.SmallIntegerField(default=None, null=True, blank=True)
    division = models.CharField(max_length=3, choices=TOUCH_DIVISION_CHOICES)
    country = CountryField()
    circuit = models.CharField(max_length=30, default="oficial", choices=CIRCUIT)
    person = models.ForeignKey(Person, related_name="person", on_delete=models.DO_NOTHING,
                               null=True, blank=True, default=None)
    position = models.PositiveSmallIntegerField(default=None, null=True, blank=True)
    tournaments_played = models.PositiveSmallIntegerField(default=0)


def get_padel_ranking(federation, division=None,  date=None):

    if date is None:
        date = get_last_ranking_date()

    if date is None:
        date = get_padel_raking_default_date()

    if division is None:
        if federation == 'Germany':
            division = MO
        elif federation == 'Thailand':
            division = O

    if division is None:
        division = get_padel_ranking_default_division(federation)

    return PadelRanking.objects.filter(
        country=federation, division=division, date=date).order_by('-points')[:200]


def get_padel_raking_default_date():
    return last_monday()


def get_padel_ranking_default_division(federation):
    if federation.upper() == 'GERMANY':
        division = MO
    elif federation.upper() == 'THAILAND':
        division = O
    return division


def get_person_padelranking(player, country, division, limit):
    import datetime
    return PadelRanking.objects.filter(
        person=player,
        country=country,
        division=division,
        date__lte=datetime.date.today()
    ).order_by('-date')[:limit]


def _padelranking_chatjs_help(dictionary, divisions):
    """
    Receive a dictionary where the keys are (country, division) and returns
    another ditionary ordered its by divisions.
    The ranking chart has to be displayed by most important divisions to
    less important divisions
    """
    result = OrderedDict()
    for division in divisions:
        for key in list(dictionary.keys()):
            if key[1] == division:
                result[key] = dictionary.pop(key)
    return result


def get_person_ranking2(player):
    result = dict()
    # find keys (player could have different rankings)
    keys = list(PadelRanking.objects.filter(
        person=player).values('country', 'division').distinct())
    # find different rankings
    for key in keys:
        ranking = get_person_padelranking(
            player, key['country'], key['division'], 52)
        # convert to suitable JS format
        js_dict = OrderedDict()
        for r in ranking:
            if js_dict.get(r.date):
                js_dict[r.date].extend([r.division, r.points, r.position])
            else:
                js_dict[r.date] = [r.date, r.division, r.points, r.position]
        result[(key['country'], key['division'])] = js_dict.values()

    sorted_result = _padelranking_chatjs_help(result, order_divisions)

    return next(iter(sorted_result.values()))


def get_person_ranking(player):
    import datetime

    result = OrderedDict()
    get_person_ranking2(player)

    ranking = PadelRanking.objects.filter(
        person=player,
        date__lte=datetime.date.today()
    ).order_by('-date', 'division')[:52]

    for r in ranking:
        if result.get(r.date):
            result[r.date].extend([r.division, r.points, r.position])
        else:
            result[r.date] = [r.date, r.division, r.points, r.position]

    return result.values()


def get_played_tournaments_per_ranking_year(padelranking_list, date, division=MO):

    result = list()
    try:
        end_date = datetime.strptime(date, "%Y-%m-%d").date()
    except TypeError:
        end_date = date
    begin_date = end_date - timedelta(days=364)

    for ranking in padelranking_list:
        tournaments = set()
        teams = set()
        players = list(Player.objects.filter(person=ranking.person.id))

        for p in players:
            teams.add(p.team)

        for t in teams:
            tournaments = tournaments | set(Tournament.objects.filter(
                teams__id=t.id, division=division, date__range=[begin_date,end_date])
                .order_by('-date', '-name'))

        ranking.tournaments_played = len(tournaments)
        result.append(ranking)

    return result


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


def get_clubs(federation):
    return Club.objects.filter(federation=federation.upper()).order_by('city')


def get_padel_tournament(id):
    return Tournament.objects.get(pk=id)


def get_padel_tournaments(federation='ALL', year=None, division=None):
    if year == 'ALL':
        year = None
    if division == 'ALL':
        division = None

    if year and division is None:
        return Tournament.objects.order_by('-date', 'city').filter(federation=federation.upper()).filter(date__year=year)
    elif year is None and division:
        return Tournament.objects.order_by('-date', 'city').filter(federation=federation.upper()).filter(division=division)
    elif year and division:
        return Tournament.objects.order_by('-date', 'city').filter(federation=federation.upper()).filter(date__year=year).filter(division=division)
    else:
        return Tournament.objects.order_by('-date', 'city').filter(federation=federation.upper())


def translate_division(division):
    translations = {'MO': _('Men'), 'WO': _('Women'), 'XO': _('Mixed'), 'MXO': _('Mixed'), 'O': _('Open'),
                    'M35': _('Men 35'), 'M40': _('Men 40'), 'M45': _('Men 45'),
                    'W40': _('Women 40'), 'X40': _('Mixed 40'), 'SMX': _('Senior Mixed')}
    return translations[division]


def get_similar_tournaments(t_id):
    result = dict()
    tournament = get_padel_tournament(t_id)
    if tournament.date:
        similars = Tournament.objects.filter(date=tournament.date, city=tournament.city)
        for t in similars:
            if t.id != tournament.id:
                result[str(t.padel_serie) + ' ' + str(translate_division(t.division))] = t.id
    return result


def normalize(filename):
    return "".join([c for c in filename if c.isalpha() or c.isdigit() or c == ' ']).rstrip()


def no_german_chars(string):
    chars = {'ö': 'oe', 'ä': 'ae', 'ü': 'ue', 'ß': 'ss'}
    for c in chars:
        string = string.replace(c, chars[c])
    return string


def last_monday():
    d = datetime.now().date()
    d -= timedelta(days=d.weekday())
    return d


def total_tournaments():
    return Tournament.objects.all().count()


def total_clubs():
    return Club.objects.filter(old=False).count()


def total_persons():
    return Person.objects.all().count()


def total_rankings():
    return PadelRanking.objects.values('division').distinct().count()


def total_courts():
    from django.db.models import Sum, F
    return Club.objects.filter(old=False).aggregate(total=Sum(F('indoor_courts') + F('outdoor_courts')))['total']
