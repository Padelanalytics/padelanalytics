""" Django command line for reading and import csvs files

This scripts allows the user to read csv files and import the readed data into the database.
The idea is to have all the statidistical data in csv files (tournaments, players, rankings) and
extend this files with new information (new tournament or ranking) or fix any mistake on the
information on the files (e.g. wrong player name or game result) and afterwards delete all the
stadistical data from the database and import it from zero again.
"""


from django.core.management.base import BaseCommand

from tournaments import csvReader


class Command(BaseCommand):
    help = 'Add csv data to the database.'

    def add_arguments(self, parser):
        parser.add_argument(
            'type', choices=['games', 'phases', 'stats_game', 'stats_tournament', 'padel', 'person', 'padel_ranking',
            'player_club', 'club'])
        parser.add_argument('file_path', nargs='+')

    def handle(self, *args, **options):
        csv_type = options['type']
        file_path = options['file_path'][0]

        self.stdout.write(self.style.SUCCESS('Read csv file: "%s"' % file_path))

        if csv_type == 'stats_game':
            reader = csvReader.CsvReader(csvReader.CsvReader.NTS_STATISTIC)
            reader.read_file(file_path)
        elif csv_type == 'stats_tournament':
            reader = csvReader.CsvReader(csvReader.CsvReader.FIT_STATISTIC)
            reader.read_file(file_path)
        elif csv_type == 'games':
            # imports touch/soccer games, creating tournaments, teams, player and persons
            # while importing
            reader = csvReader.CsvReader(csvReader.CsvReader.TOURNAMENT)
            reader.read_file(file_path)
        elif csv_type == 'padel':
            # imports padel games, creating tournaments, teams, player and persons while importing
            reader = csvReader.CsvReader(csvReader.CsvReader.PADEL_GAME)
            reader.read_file(file_path)
        elif csv_type == 'phases':
            # import phases of a game
            reader = csvReader.CsvReader(csvReader.CsvReader.PHASE)
            reader.read_file(file_path)
        elif csv_type == 'person':
            reader = csvReader.CsvReader(csvReader.CsvReader.PERSON)
            reader.read_file(file_path)
        elif csv_type == 'padel_ranking':
            # imports a padel ranking, creating a persons while importing
            reader = csvReader.CsvReader(csvReader.CsvReader.PADEL_RANKING)
            reader.read_file(file_path)
        elif csv_type == 'player_club':
            # add clubs to the player model
            reader = csvReader.CsvReader(csvReader.CsvReader.PADEL_PLAYER_CLUB)
            reader.read_file(file_path)
        elif csv_type == 'club':
            # add clubs to the club model
            reader = csvReader.CsvReader(csvReader.CsvReader.CLUB)
            reader.read_file(file_path)
        else:
            raise Exception('Argument %s not supported.' % csv_type)

        self.stdout.write(self.style.SUCCESS('Successfully read csv file: "%s"' % file_path))
