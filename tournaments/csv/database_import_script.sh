#!/bin/bash
# Coppyright (c) 2015 Francisco Javier Revilla Linares to present.
# All rights reserved.

## This script delete the tournaments, players and ranking of the database as well as
## resets the indexes of the deleted objects. After deleting all the data, the script imports
## first the tournaments year by year and finally the ranking.

## With the option --no-ranking as a optional third argument the scripts do not import
## the ranking.

## To execute this script, first change if necessary the constants wit the ranking files:
## GER_RANKING, THA_RANKING and SWI_RANKING
## Afterwards execute the command:
## bash ./tournaments/csv/database_import_script.sh /home/paconte/devel/padelanlytics
## or
## bash ./tournaments/csv/database_import_script.sh /home/paconte/devel/padelanlytics --no-ranking


## To help to understand the script, it perform the below manual commands, in case the user
## prefers to use the command line by itselfs:
:'
sqlite3 padelanalytics/db.sqlite3 < tournaments/csv/delete_data.sql
python3 manage.py readcsv phases /home/paconte/devel/padelanalytics/tournaments/csv/Tournament_Phases.csv
python3 manage.py readcsv padel /home/paconte/devel/padelanlytics/tournaments/csv/Padel_Tournaments_HOL_2018_utf8.csv
sqlite3 padelanalytics/db.sqlite3 < tournaments/csv/tournaments_update.sql
'


# set debug mode and exit on error
set -x
set -e


##### constants

PROJECT_PATH=$1
DATABASE_PATH=$PROJECT_PATH"/padelanalytics/db.sqlite3"
CSV_PATH=$PROJECT_PATH"/tournaments/csv/"
PYTHON3_COMMAND=$(which python3)
SQLITE3_COMMAND=$(which sqlite3)

GER_RANKING="GER_ranking_20200330.csv"
THA_RANKING="THA_ranking_2019_utf8.csv"
SWI_RANKING="SWI_ranking_20200301.csv"
WPT_RANKING="WPT_ranking_20200330.csv"


##### functions

delete_database_objects() {
    local FILE="delete_data.sql"
    local PATH="$CSV_PATH$FILE"
    $SQLITE3_COMMAND $DATABASE_PATH < $PATH
} # end of delete_database_objects


import_phases() {
    local FILE="tournaments_phases.csv"
    local PATH="$CSV_PATH$FILE"
    $PYTHON3_COMMAND manage.py readcsv phases $PATH
} # end of import_phases


import_clubs() {
    local FILE1="NED_clubs_utf8.csv"
    local FILE2="SWI_clubs_utf8.csv"
    $PYTHON3_COMMAND manage.py readcsv club "$CSV_PATH$FILE1"
    $PYTHON3_COMMAND manage.py readcsv club "$CSV_PATH$FILE2"
}


import_german_tournaments() {
    local FILE1="GER_tournaments_2015_utf8.csv"
    local FILE2="GER_tournaments_2016_utf8.csv"
    local FILE3="GER_tournaments_2017_utf8.csv"
    local FILE4="GER_tournaments_2018_utf8.csv"
    local FILE5="GER_tournaments_2019_utf8.csv"
    local FILE6="GER_tournaments_2020_utf8.csv"
    $PYTHON3_COMMAND manage.py readcsv padel $CSV_PATH$FILE1
    $PYTHON3_COMMAND manage.py readcsv padel $CSV_PATH$FILE2
    $PYTHON3_COMMAND manage.py readcsv padel $CSV_PATH$FILE3
    $PYTHON3_COMMAND manage.py readcsv padel $CSV_PATH$FILE4
    $PYTHON3_COMMAND manage.py readcsv padel $CSV_PATH$FILE5
    $PYTHON3_COMMAND manage.py readcsv padel $CSV_PATH$FILE6
} # end of import_german_tournaments


import_netherlands_tournaments() {
    local FILE1="NED_tournaments_2018_utf8.csv"
    local FILE2="NED_tournaments_2019_utf8.csv"
    $PYTHON3_COMMAND manage.py readcsv padel $CSV_PATH$FILE1
    $PYTHON3_COMMAND manage.py readcsv padel $CSV_PATH$FILE2
} # end of import_thailand_tournaments


import_thailand_tournaments() {
    local FILE1="THA_tournaments_2019_utf8.csv"
    $PYTHON3_COMMAND manage.py readcsv padel $CSV_PATH$FILE1
} # end of import_thailand_tournaments


import_wpt_tournaments() {
    local FILE1="WPT_tournaments_2018_utf8.csv"
    local FILE2="WPT_tournaments_2019_utf8.csv"
    local FILE3="WPT_tournaments_2020_utf8.csv"
    $PYTHON3_COMMAND manage.py readcsv padel $CSV_PATH$FILE1
    $PYTHON3_COMMAND manage.py readcsv padel $CSV_PATH$FILE2
    $PYTHON3_COMMAND manage.py readcsv padel $CSV_PATH$FILE3

} # end of import_wpt_tournaments


import_players_club() {
    local FILE1="GER_players_clubs_utf8.csv"
    local FILE2="THA_players_clubs_utf8.csv"
    local FILE3="NED_players_clubs_utf8.csv"
    local FILE4="SWI_players_clubs_utf8.csv"
    local FILE5="WPT_players_clubs_utf8.csv"
    $PYTHON3_COMMAND manage.py readcsv player_club "$CSV_PATH$FILE1"
    $PYTHON3_COMMAND manage.py readcsv player_club "$CSV_PATH$FILE2"
    $PYTHON3_COMMAND manage.py readcsv player_club "$CSV_PATH$FILE3"
    $PYTHON3_COMMAND manage.py readcsv player_club "$CSV_PATH$FILE4"
    $PYTHON3_COMMAND manage.py readcsv player_club "$CSV_PATH$FILE5"
} # end of import_players_club


update_tournaments_info() {
    local FILE="tournaments_update.sql"
    $SQLITE3_COMMAND $DATABASE_PATH < "$CSV_PATH$FILE"
} # end of update_tournaments_info


import_german_ranking() {
    $PYTHON3_COMMAND manage.py readcsv padel_ranking "$CSV_PATH$GER_RANKING"
} # end of import_german_ranking


import_thailand_ranking() {
    $PYTHON3_COMMAND manage.py readcsv padel_ranking "$CSV_PATH$THA_RANKING"
} # end of import_thailand_ranking


import_switzerland_ranking() {
    $PYTHON3_COMMAND manage.py readcsv padel_ranking "$CSV_PATH$SWI_RANKING"
} # end of import_switzerland_ranking

import_wpt_ranking() {
    $PYTHON3_COMMAND manage.py readcsv padel_ranking "$CSV_PATH$WPT_RANKING"
} # end of import_switzerland_ranking


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
    import_netherlands_tournaments
    import_thailand_tournaments
    import_wpt_tournaments

    # update tournament info
    update_tournaments_info

    # exits if no ranking option is activated
    if [ $NO_RANKING ] ; then
        exit 0
    fi

    # import ranking
    import_german_ranking
    import_switzerland_ranking
    import_thailand_ranking
    import_wpt_ranking

    # import clubs and players clubs and countroes
    import_clubs
    import_players_club

    # compute ranking positions
    compute_ranking_positions

    # compute ranking tournaments (not working well at the moment)
    #compute_ranking_tournaments

} # end of import_database


##### Main

if  [ "$#" -eq 1 ] ; then    # one argument
    import_database

elif [ "$#" -eq 2 ] ; then   # two arguments

    if [ "$2" = "--no-ranking" ] ; then
        NO_RANKING=true
        import_database
    else
        echo "Illegal parameter: $2. It must be empty or --no-ranking"
        exit 1
    fi

else                          # incorrect number of afguments
    echo "Illegal number of arguments"
    exit 1
fi
