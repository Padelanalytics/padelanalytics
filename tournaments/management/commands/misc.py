from django.core.management.base import BaseCommand

from tournaments.helpers import compute_ranking_positions, compute_ranking_tournaments


class Command(BaseCommand):
    compute_ranking_positions = "compute_ranking_positions"
    compute_ranking_tournaments = "compute_ranking_tournaments"

    help = "Miscellaneous helping tools for the tournaments app."

    def add_arguments(self, parser):
        parser.add_argument(
            "option",
            choices=["compute_ranking_positions", "compute_ranking_tournaments"],
        )

    def handle(self, *args, **options):
        opt = options["option"]
        if opt == "compute_ranking_positions":
            compute_ranking_positions()
        elif opt == "compute_ranking_tournaments":
            compute_ranking_tournaments()
        else:
            raise Exception("Argument %s not supported." % opt)
