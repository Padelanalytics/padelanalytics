#from decimal import Decimal

from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator
from django.db import models
from django_countries.fields import CountryField

from decimal import *
from anmeldung.validators import policy_read_validator
from tournaments.models import Club
from tournaments.models import Person
from tournaments.models import Tournament
from tournaments.models import normalize
from tournaments.models import no_german_chars


CATEGORY_GERMANY = (('Herren A', 'Herren A'), ('Herren B', 'Herren B'), ('Damen', 'Damen'), ('Mixed', 'Mixed'),
                    ('Senioren', 'Senioren'), ('Junioren', 'Junioren'))
PLAYER = (('A', 'A'), ('B', 'B'))


def player_directory_path(instance, filename):
    return 'player_media/' + normalize(no_german_chars(
        '{0}-{1}-{2}-{3}'.format(instance.last_name, instance.first_name, instance.email, filename)))


class PadelPerson(Person):
    last_name2 = models.CharField(max_length=24, blank=True)
    email = models.EmailField(verbose_name='Email')
    phone = models.CharField(max_length=64, verbose_name='Phone')
    city = models.CharField(max_length=32, verbose_name='City')
    club = models.ForeignKey(Club, on_delete=models.DO_NOTHING)
    birthplace = models.CharField(max_length=32, verbose_name='Birth place')
    ranking_points = models.DecimalField(
        max_digits=6, decimal_places=1, validators=[MinValueValidator(Decimal('0.0'))], default=Decimal('0.0'))
    photo = models.ImageField(upload_to=player_directory_path, default='Cool-Male-Avatars-06.png')
    policy_read_a = models.BooleanField(default=False, validators=[policy_read_validator])
    policy_read_b = models.BooleanField(default=False, validators=[policy_read_validator])
    policy_read_c = models.BooleanField(default=False, validators=[policy_read_validator])

    def __str__(self):
        return " ".join([str(self.first_name), str(self.last_name)])

    def abbr(self):
        return " ".join([self.first_name[0] + '.', self.last_name])


class Registration(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True, editable=False)
    tournament = models.ForeignKey(Tournament, on_delete=models.DO_NOTHING)
    player_a = models.ForeignKey(PadelPerson, related_name="player_a", on_delete=models.DO_NOTHING)
    player_b = models.ForeignKey(PadelPerson, related_name="player_b", on_delete=models.DO_NOTHING)
    is_active_a = models.BooleanField(default=False)
    is_active_b = models.BooleanField(default=False)

    def __str__(self):
        return " - ".join([str(self.player_a), str(self.player_b)])

    def is_active(self):
        return self.is_active_a and self.is_active_b


def get_all_registrations(tournament_id):
    return Registration.objects.filter(tournament=tournament_id)


def get_tournament_teams_by_ranking(tournament_id):
    teams = Registration.objects.filter(tournament=tournament_id, is_active_a=True, is_active_b=True)
    result = list()
    for team in teams:
        ranking = team.player_a.ranking_points + team.player_b.ranking_points
        result.append((team, ranking))
    return sorted(result, key=lambda x: x[1], reverse=True)



