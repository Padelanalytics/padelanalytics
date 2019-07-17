from django.core.management.base import BaseCommand
from tournaments.service import compute_ranking

class Command(BaseCommand):

    compute_ranking = 'compute_ranking'
    
    help = 'Miscellaneous helping tools for the tournaments app.'

    def add_arguments(self, parser):
        parser.add_argument('option', choices=['compute_ranking'])
        
    def handle(self, *args, **options):
        opt = options['option']
        if opt == 'compute_ranking':
            compute_ranking()
        else:
            raise Exception('Argument %s not supported.' % opt)
