# Django migrations

Because most of the data is in csv and can be imported, there are not much migrations and eventually the init file for migrations is recreated.

## Known issues

After creating the migrations for the first time two different django.db.utils.IntegrityError are thrown. Below the examples:


```sh
django.db.utils.IntegrityError: The row in table 'tournaments_team' with primary key '2832' has an invalid foreign key: tournaments_team.club_id contains a value '246' that does not have a corresponding value in tournaments_club.id.
```

```sh
  File "/Users/frevilla/dev/other/padelanalytics/.venv/padel/lib/python3.13/site-packages/django/db/backends/sqlite3/schema.py", line 39, in __exit__
    self.connection.check_constraints()
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/Users/frevilla/dev/other/padelanalytics/.venv/padel/lib/python3.13/site-packages/django/db/backends/sqlite3/base.py", line 298, in check_constraints
    raise IntegrityError(
    ...<12 lines>...
    )
django.db.utils.IntegrityError: The row in table 'tournaments_player_tournaments_played' with primary key '9764' has an invalid foreign key: tournaments_player_tournaments_played.player_id contains a value '8586' that does not have a corresponding value in tournaments_player.id.
```

This needs to be investigated, because there are tournaments with players that does not exists. The reason is at this moment unknown.

To fix the this constraint you can run the following query:

```sh
padelanalytics % sqlite3 padelanalytics/db.sqlite3
sqlite> UPDATE tournaments_team SET club_id=null WHERE id = 2832;
sqlite> DELETE from tournaments_player_tournaments_played WHERE player_id in (SELECT player_id FROM  tournaments_player_tournaments_played as tp WHERE tp.player_id NOT IN (SELECT id FROM tournaments_player));
sqlite> .q

padelanalytics % python3 manage.py migrate

padelanalytics % sqlite3 padelanalytics/db.sqlite3
sqlite> UPDATE tournaments_tournament SET game_type="MULTI" WHERE id IN (421, 422, 423, 424, 452, 472);
sqlite> .q

python manage.py readcsv phases ./tournaments/csv/production/tournaments_phases.csv
python3 manage.py readcsv padel ./tournaments/csv/HiPadel_tournaments_2025_utf8.csv

padelanalytics % sqlite3 padelanalytics/db.sqlite3
sqlite> UPDATE tournaments_tournament SET game_type=SINGLE WHERE id=475;
```