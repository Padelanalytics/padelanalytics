# Coppyright (c) 2025 Francisco Javier Revilla Linares
# All rights reserved.

import logging

from datetime import datetime, timedelta
from tournaments.models import PadelRanking, Player, Tournament


logger = logging.getLogger(__name__)


def ranking_to_chartjs(ranking):
    """
    Extract the required data for representing a ranking with chart.js at
    the frontend.
    """
    # total_of_rankings = (len(next(iter(ranking)))-1)/2
    dates = []
    points = []
    positions = []

    for r in ranking:
        dates.append(r[0])
        points.append(r[2])
        positions.append(r[3])

    dates.reverse()
    points.reverse()
    positions.reverse()

    return dates, points, positions


def last_monday(date=None):
    """
    Returns the last monday since the current operating system date. Or the last monday since
    the fiven date argument. If current date is Monday then current date is returned.
    """
    from datetime import datetime, timedelta

    if date:
        d = date
    else:
        d = datetime.now().date()
    d -= timedelta(days=d.weekday())
    return d


def all_mondays_from_to(from_date, to_date, tuple=False):
    """
    Returns all the mondays from the given date from_date until the last monday after the given
    date to_date
    """
    result = []

    if from_date.weekday() != 0:
        from_date += timedelta(days=7 - from_date.weekday())

    while from_date <= to_date:
        result.append((from_date, from_date)) if tuple else result.append(from_date)
        from_date += timedelta(days=7)

    return result


def all_mondays_from(d, tuple=False):
    """
    Returns all the mondays from the given date d until the last monday of the
    current year where the operatym system runs
    """
    result = []
    current_year = datetime.now().year

    if d.weekday() != 0:
        d += timedelta(days=7 - d.weekday())

    while d.year <= current_year:
        result.append((d, d)) if tuple else result.append(d)
        d += timedelta(days=7)

    return result


def all_mondays_since(year):
    current_year = datetime.now().year
    d = datetime.date(year, 1, 1)  # First January
    d += timedelta(days=(7 - d.weekday()) % 7)  # First Monday
    while year <= d.year <= current_year:
        yield (d, d)
        d += timedelta(days=7)


def compute_ranking_positions():
    padel_ranking = PadelRanking.objects.all().order_by(
        "-country", "-circuit", "-division", "-date", "-points"
    )

    first = padel_ranking.first()
    position = 1
    position_aux = 1
    division = first.division
    date = first.date
    points = first.points
    country = first.country
    for ranking in padel_ranking:
        # new ranking calculation
        if ranking.division != division or ranking.date != date or ranking.country != country:
            points = ranking.points
            country = ranking.country
            division = ranking.division
            date = ranking.date
            position = 1
            position_aux = 1
        # calculate next position
        if points > ranking.points:
            position = position_aux
            points = ranking.points
        position_aux += 1
        ranking.position = position
        ranking.save()


def compute_ranking_tournaments():
    padel_ranking = PadelRanking.objects.all()
    for ranking in padel_ranking:
        _compute_played_tournaments_per_ranking_year(ranking)


def _compute_played_tournaments_per_ranking_year(ranking):
    try:
        end_date = datetime.strptime(ranking.date, "%Y-%m-%d").date()
    except TypeError:
        end_date = ranking.date
    begin_date = end_date - timedelta(days=364)

    tournaments = set()
    teams = set()
    players = list(Player.objects.filter(person=ranking.person.id))

    for p in players:
        teams.add(p.team)

    for t in teams:
        tournaments = tournaments | set(
            Tournament.objects.filter(
                teams__id=t.id,
                division=ranking.division,
                date__range=[begin_date, end_date],
            ).order_by("-date", "-name")
        )

    ranking.tournaments_played = len(tournaments)
    ranking.save()
