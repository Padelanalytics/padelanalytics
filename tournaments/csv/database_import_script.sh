#!/bin/bash

## This script delete the tournaments, players and ranking of the database as well as
## resets the indexes of the deleted objects. After deleting all the data, the script imports
## first the tournaments year by year and finally the ranking.

## With the option --no-ranking as a optional third argument the scripts do not import
## the ranking.

## To help to understand the script, it perform the below manual commands, in case the user
## prefers to use the command line by itselfs:
:'
sqlite3 padelanalytics/db.sqlite3 < tournaments/csv/delete_data.sql
python3 manage.py readcsv phases /home/paconte/devel/padelanalytics/tournaments/csv/Tournament_Phases.csv
python3 manage.py readcsv padel /home/paconte/devel2/padelanlytics/tournaments/csv/Padel_Tournaments_2015_utf8.csv
python3 manage.py readcsv padel /home/paconte/devel2/padelanlytics/tournaments/csv/Padel_Tournaments_2016_utf8.csv
python3 manage.py readcsv padel /home/paconte/devel2/padelanlytics/tournaments/csv/Padel_Tournaments_2017_utf8.csv
python3 manage.py readcsv padel /home/paconte/devel2/padelanlytics/tournaments/csv/Padel_Tournaments_2018_utf8.csv
python3 manage.py readcsv padel /home/paconte/devel2/padelanlytics/tournaments/csv/Padel_Tournaments_2019_utf8.csv
sqlite3 padelanalytics/db.sqlite3 < tournaments/csv/tournaments_update.sql
python3 manage.py readcsv padel_ranking /home/paconte/devel2/padelanlytics/tournaments/csv/PA_Ranking_201907022.csv
python3 manage.py misc compute_ranking
'

# set debug mode and exit on error
set -x
set -e

##### constants

PROJECT_PATH=$1
CURRENT_RANKING=$2
DATABASE_PATH=$PROJECT_PATH"/padelanalytics/db.sqlite3"
CSV_PATH=$PROJECT_PATH"/tournaments/csv/"
PYTHON3_COMMAND=$(which python3)
SQLITE3_COMMAND=$(which sqlite3)

##### functions

delete_database_objects() {
    local FILE="delete_data.sql"
    local PATH="$CSV_PATH$FILE"
    $SQLITE3_COMMAND $DATABASE_PATH < $PATH
} # end of delete_database_objects

import_phases() {
    local FILE="Tournament_Phases.csv"
    local PATH="$CSV_PATH$FILE"
    $PYTHON3_COMMAND manage.py readcsv phases $PATH
} # end of import_phases

import_german_tournaments() {
    local FILE1="Padel_Tournaments_2015_utf8.csv"
    local FILE2="Padel_Tournaments_2016_utf8.csv"
    local FILE3="Padel_Tournaments_2017_utf8.csv"
    local FILE4="Padel_Tournaments_2018_utf8.csv"
    local FILE5="Padel_Tournaments_2019_utf8.csv"
    $PYTHON3_COMMAND manage.py readcsv padel $CSV_PATH$FILE1
    $PYTHON3_COMMAND manage.py readcsv padel $CSV_PATH$FILE2
    $PYTHON3_COMMAND manage.py readcsv padel $CSV_PATH$FILE3
    $PYTHON3_COMMAND manage.py readcsv padel $CSV_PATH$FILE4
    $PYTHON3_COMMAND manage.py readcsv padel $CSV_PATH$FILE5
} # end of import_german_tournaments

update_german_tournaments() {
    local FILE="tournaments_update.sql"
    $SQLITE3_COMMAND $DATABASE_PATH < "$CSV_PATH$FILE"
} # end of update_german_tournaments

import_german_ranking() {
    $PYTHON3_COMMAND manage.py readcsv padel_ranking "$CSV_PATH$CURRENT_RANKING"
} # end of import_german_ranking

compute_ranking_positions() {
    $PYTHON3_COMMAND manage.py misc compute_ranking_positions
} # end of compute_ranking_positions

compute_ranking_tournaments() {
    $PYTHON3_COMMAND manage.py misc compute_ranking_tournaments
} # end of compute_ranking_tournaments

import_database() {
    # delete database and indexes
    delete_database_objects
    # import tournament phases
    import_phases
    # import all tournaments year by year
    import_german_tournaments
    # update tournament info
    update_german_tournaments
    # exits if no ranking option is activated
    if [ $NO_RANKING ] ; then
        exit 0
    fi
    # import ranking
    import_german_ranking
    # compute ranking positions
    compute_ranking_positions
    # compute ranking tournaments
    compute_ranking_tournaments
} # end of import_database


##### Main

if  [ "$#" -eq 2 ] ; then    # two arguments
    import_database

elif [ "$#" -eq 3 ] ; then   # three arguments

    if [ "$3" = "--no-ranking" ] ; then
        NO_RANKING=true
        import_database
    else
        echo "Illegal parameter: $3. It must be empty or --no-ranking"
        exit 1
    fi

else                          # incorrect number of afguments
    echo "Illegal number of arguments"
    exit 1
fi
