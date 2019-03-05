from django.core.management.base import BaseCommand
from tournaments.models import Tournament
from anmeldung.models import PadelTournament


class Command(BaseCommand):
    help = 'Synchronize tables from anmeldung with tournaments tables.'

    def add_arguments(self, parser):
        parser.add_argument('sync', choices=['tournaments'])

    def handle(self, *args, **options):
        sync = options['sync']

        if sync == 'tournaments':
            tournaments = Tournament.objects.all()
            padel_tournaments = PadelTournament.objects.all()

            for t in tournaments:
                found = False
                for pt in padel_tournaments:
                    if pt.tournament == t:
                        found = True
                        break
                if not found:
                    new_tournament = PadelTournament(tournament_ptr=t)
                    new_tournament.save()
                    print("Created new PadelTournament %s" % new_tournament)
        else:
            raise Exception('Argument %s not supported.' % sync)

