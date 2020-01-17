import logging

from collections import OrderedDict

from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.template.exceptions import TemplateDoesNotExist

from anmeldung.models import get_tournament_teams_by_ranking
from anmeldung.models import get_all_registrations
from anmeldung.forms import RankingForm, RegistrationForm, SearchForm, TournamentsForm
from anmeldung.forms import RegistrationForm
from anmeldung.tokens import account_activation_token

from tournaments.models import Game, Person, Player, Team, Tournament
from tournaments.models import get_tournament_games
from tournaments.models import get_padel_tournament_teams
from tournaments.models import get_padel_tournament
from tournaments.models import get_padel_tournaments
from tournaments.models import get_padel_ranking
from tournaments.models import get_person_ranking
from tournaments.models import get_clubs
from tournaments.models import get_last_ranking_date
from tournaments.models import get_similar_tournaments
from tournaments.models import total_clubs
from tournaments.models import total_tournaments
from tournaments.models import total_rankings
from tournaments.models import total_persons
from tournaments.models import total_courts
from tournaments.service import Fixtures, ranking_to_charjs


# Get an instance of a logger
logger = logging.getLogger(__name__)


def index(request):
    return render(request, 'landing.html',
                  {'total_clubs': total_clubs(),
                   'total_tournaments': total_tournaments(),
                   'total_rankings': total_rankings(),
                   'total_persons': total_persons(),
                   'total_courts': total_courts()})


def test_view(request):
    #return render(request, 'tournament_signup_success.html',
    #            {'email_a': 'paco@gmail.com',
    #             'email_b': 'fran@gmail.com',
    #             'from_email': 'info@padelanalytics.com'
    #             })
    #return render(request, 'tournament_signup_activation.html', {'tournament_id': 5})
    #return render(request, 'activation_failed.html')
    #return render(request, '404.html')
    return render(request, '500.html')
    #return render(request, 'new_player_success.html')


def news(request, id):
    template = 'news/news_' + str(id) + '.html'
    try:
        return render(request, template)
    except TemplateDoesNotExist:
        return render(request, '404.html')


def tournament_signup(request, id=None):
    return render(request, '404.html')
    if request.method == 'POST':
        registration_form = RegistrationForm(request.POST)
        if registration_form.is_valid():
            player_a = registration_form.cleaned_data['player_a']
            player_b = registration_form.cleaned_data['player_b']
            tournament = registration_form.cleaned_data['tournament']

            # check tournament signup is on
            if tournament.signup == False:
                registration_form.add_error('tournament', 'This tournament is not open to registrations.')
                return render(request, 'tournament_signup.html', {'form': registration_form})

            # check player is not twice in the team
            if player_a.id == player_b.id:
                registration_form.add_error('player_b', 'A team must have two different players.')
                return render(request, 'tournament_signup.html', {'form': registration_form})

            # check no player is twice in a tournament
            registrations = get_all_registrations(registration_form.cleaned_data['tournament'])
            for reg in registrations:
                if player_a.id == reg.player_a.id or player_a.id == reg.player_b.id:
                    registration_form.add_error('player_a', 'Player already signed up in the tournament.')
                    return render(request, 'tournament_signup.html', {'form': registration_form})
                elif player_b.id == reg.player_a.id or player_b.id == reg.player_b.id:
                    registration_form.add_error('player_b', 'Player already signed up in the tournament.')
                    return render(request, 'tournament_signup.html', {'form': registration_form})

            # all checks are good
            registration = registration_form.save()
            # send activation email
            from django.conf import settings
            from_email = settings.DEFAULT_FROM_EMAIL
            cc_email = settings.DEFAULT_CC_EMAIL
            current_site = get_current_site(request)
            _send_activation_email(current_site, registration, player_a, from_email, player_a.email, cc_email)
            _send_activation_email(current_site, registration, player_b, from_email, player_b.email, cc_email)

            return render(request, 'tournament_signup_success.html',
                          {'email_a': player_a.email,
                           'email_b': player_b.email,
                           'from_email': from_email
                           })
        # form is invalid
        else:
            return render(request, 'tournament_signup.html', {'form': registration_form})
    else:
        if id:
            form = RegistrationForm(initial={'tournament': id})
        else:
            form = RegistrationForm()
        form.fields['tournament'].queryset = Tournament.objects.filter(signup=True)
        return render(request, 'tournament_signup.html', {'form': form})


def tournaments(request):
    return render(request, 'pretournaments.html')


def tournaments_federation(request, federation):
    tournaments = get_padel_tournaments(federation=federation)
    if request.method == 'POST':
        form = TournamentsForm(request.POST)
        if form.is_valid():
            year = form.cleaned_data['year']
            division = form.cleaned_data['division']
            tournaments = get_padel_tournaments(federation, year, division)
    else:
        form = TournamentsForm()

    return render(
        request,
        'turnierliste.html',
        {'federation': federation, 'tournaments': tournaments, 'form': form})


def tournament(request, id):
    # partidos, equipos_de_verdad, equipos_anmeldeados,
    # num_de_pools, num_de_goldsilver_en_ko, num_de_ko_runde
    tournament = get_padel_tournament(id)
    similar_tournaments = get_similar_tournaments(id)
    signed_up_teams = get_tournament_teams_by_ranking(id)

    all_games = get_tournament_games(tournament)
    real_teams = get_padel_tournament_teams(tournament)
    fixtures = Fixtures(all_games)
    pool_games = fixtures.pool_games
    pool_tables = fixtures.sorted_pools
    ko_games = fixtures.get_phased_finals({})
    # get the first round of the ko phase:
    ko_round_start = None
    if len(ko_games) > 0:
        k, v = next(iter(ko_games.items()))
        ko_round_start = next(iter(v)).round

    return render(
        request,
        'tournament.html',
        {
            'tournament': tournament,
            'similar_tournaments': similar_tournaments,
            'signed_up_teams': signed_up_teams,
            'real_teams': real_teams,
            'pool_tables': pool_tables,
            'pool_games': pool_games,
            'ko_games': ko_games,
            'ko_round_start': ko_round_start
        })


def clubs(request):
    return render(request, 'preclubs.html')


def clubs_federation(request, federation):
    clubs = get_clubs(federation)
    return render(
        request, 'clubs.html', {'federation': federation, 'clubs': clubs})


def new_player(request):
    return render(request, '404.html')
    """
    new_player_form = get_new_player_form()
    if request.method == 'POST':
        new_player_form = new_player_form(request.POST)
        if new_player_form.is_valid():
            # get or create the person
            person, created = Person.objects.get_or_create(
                first_name=new_player_form.cleaned_data[0]['first_name'],
                last_name=new_player_form.cleaned_data[0]['last_name'],
                born=new_player_form.cleaned_data[0]['born'],
                nationality=None,
                gender=new_player_form.cleaned_data[0]['gender']
            )
            # logging
            if created:
                logger.info("While creating a new PadelPerson a new Person has been created: %s", person)
            # saving the new PadelPerson
            padel_person = new_player_form.save(commit=False)[0]
            padel_person.person_ptr = person
            padel_person.save()
            return render(request, 'new_player_success.html')
        else:
            return render(request, 'new_player.html', {'formset': new_player_form})
    else:
        return render(request, 'new_player.html', {'formset': new_player_form})
    """


def ranking(request):
    return render(request, 'preranking.html')


def ranking_federation(request, federation):
    if request.method == 'POST':
        form = RankingForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            division = form.cleaned_data['division']
            ranking = get_padel_ranking(federation, date, division)
        else:
            ranking = None
    else:
        form = RankingForm(federation=federation)
        ranking = get_padel_ranking(federation)

    return render(
        request,
        'ranking.html',
        {'federation': federation, 'form': form, 'ranking': ranking})


def about(request):
    return render(request, 'about.html')


def player_detail(request, id):
    partners = set()
    teams = set()
    teams_ids = set()
    tournaments = set()
    games = list()
    players = list(Player.objects.filter(person=id))
    person = Person.objects.filter(pk=id)
    ranking = get_person_ranking(id)
    gr_labels, gr_points, gr_positions = ranking_to_charjs(ranking)
    #print(len(ranking))
    #print(len(gr_labels), len(gr_points), len(gr_positions))

    for p in players:
        teams.add(p.team)

    for t in teams:
        # games
        games = games + list(Game.objects.filter(Q(local=t.id) | Q(visitor=t.id)).order_by('tournament'))
        # parnerts
        for p in t.players.all().exclude(id=id):
            partners.add(p)
        # played tournaments
        tournaments = tournaments | set(Tournament.objects.filter(teams__id=t.id).order_by('-date', '-name'))

    for t in teams:
        teams_ids.add(t.id)

    games.sort()

    total_games, total_wins, total_lost, ratio, sorted_games = _calc_team_player_detail(games, teams_ids)

    return render(request, 'person.html',
                  {'partners': partners, 'tournaments': tournaments, 'games': games, 'total_games': total_games,
                   'total_tournaments': len(tournaments), 'total_wins': total_wins, 'total_lost': total_lost,
                   'ratio': round(ratio * 100, 2), 'player': person, 'sorted_games': sorted_games, 'teams': teams,
                   'ranking': ranking, 'gr_labels': gr_labels, 'gr_points': gr_points, 'gr_positions': gr_positions})


def _calc_team_player_detail(games, ids):

    total_wins = 0
    sorted_games = dict()
    total_games = len(games)

    for g in games:
        sorted_games.setdefault(g.tournament, []).append(g)
        if (g.local.id in ids and g.result_padel.winner == 1) or (g.visitor.id in ids and g.result_padel.winner == 2):
            total_wins += 1

    total_lost = total_games - total_wins
    ratio = total_wins / total_games if total_games != 0 else 0

    sorted_games2 = OrderedDict()

    for key in sorted(sorted_games.keys(), key=lambda x: x.date, reverse=True):
        sorted_games2[key] = sorted_games[key]

    return total_games, total_wins, total_lost, ratio, sorted_games2


def team_detail(request, id):
    games = list(Game.objects.filter(Q(local=id) | Q(visitor=id)).order_by('tournament'))
    games.sort()
    played_tournaments = Tournament.objects.filter(teams__id=id).order_by('-date', '-name')
    players = Player.objects.filter(team=id)
    total_games, total_wins, total_lost, ratio, sorted_games = _calc_team_player_detail(games, [id])
    total_tournaments = len(played_tournaments)

    return render(request, 'team.html',
                  {'players': players, 'tournaments': played_tournaments, 'games': games, 'total_games': total_games,
                   'total_tournaments': total_tournaments, 'total_wins': total_wins, 'total_lost': total_lost,
                   'ratio': round(ratio * 100, 2), 'sorted_games': sorted_games})


def activate(request, registration_uidb64, player_uidb64, token):
    activated = False
    try:
        player_uid = force_text(urlsafe_base64_decode(player_uidb64))
        registration_uid = force_text(urlsafe_base64_decode(registration_uidb64))
        player = PadelPerson.objects.get(pk=player_uid)
        registration = Registration.objects.get(pk=registration_uid)
    except(TypeError, ValueError, OverflowError, ObjectDoesNotExist):
        player = None
        registration = None

    if player is not None and registration is not None and account_activation_token.check_token(player, token):
        if player == registration.player_a:
            registration.is_active_a = True
            activated = True
        elif player == registration.player_b:
            registration.is_active_b = True
            activated = True

    if activated:
        registration.save()
        return render(request, 'tournament_signup_activation.html', {'tournament_id': registration.tournament.id})
    else:
        return render(request, 'activation_failed.html')


def handler404(request, exception, template_name='404.html'):
    return render(request, template_name=template_name, status=404)


def handler500(request, exception, template_name='404.html'):
    return render(request, template_name=template_name, status=500)


def _send_activation_email(current_site, registration, player, from_email, to_email, cc_email):
    message = render_to_string(
        'acc_active_email.html',
        {
            'user': player,
            'domain': current_site.domain,
            'registration_uid': urlsafe_base64_encode(force_bytes(registration.pk)).decode(),
            'player_uid': urlsafe_base64_encode(force_bytes(player.pk)).decode(),
            'token': account_activation_token.make_token(player),
        }
    )
    mail_subject = 'Activate your tournament registration.'
    email = EmailMessage(mail_subject, message, to=[to_email], from_email=from_email, cc=cc_email)
    email.send()


def circuits(request):
    return render(request, 'circuits.html')


def search(request):
    result_size = 0
    after_search = False
    teams, persons, tournaments = [], [], []

    if request.method == 'GET':
        form = SearchForm(request.GET)
        if form.is_valid():
            text = form.cleaned_data.get('text')
            if text is not None and len(text) > 0:
                teams = Team.objects.filter(name__icontains=text)
                persons = Person.objects.filter(Q(first_name__icontains=text) | Q(last_name__icontains=text))
                tournaments = Tournament.objects.filter(name__icontains=text)
                result_size = len(persons) + len(tournaments) + len(teams)
                after_search = True
        else:
            query = request.GET.get('q')
            if query and len(query) > 0:
                teams = Team.objects.filter(name__icontains=query)
                persons = Person.objects.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query))
                tournaments = Tournament.objects.filter(name__icontains=query)
                result_size = len(persons) + len(tournaments) + len(teams)
                form = SearchForm(initial={'text': query})
                after_search = True
    else:
        form = SearchForm()

    return render(
        request,
        "search.html",
        {'form': form, 'result_tournaments': tournaments, 'result_persons': persons,
        'result_teams': teams, 'result_size': result_size, 'after_search': after_search })
