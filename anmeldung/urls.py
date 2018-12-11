from django.conf import settings
from django.urls import path
from django.conf.urls import url
from django.conf.urls import include
from django.conf.urls.static import static

from anmeldung import views


handler404 = views.handler404
handler500 = views.handler500

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('test_view', views.test_view, name='test_view'),
    url(r'^$', views.index, name='index'),
    path('tournament_signup', views.tournament_signup, name='tournament_signup'),
    path('tournament_signup/<int:id>/', views.tournament_signup, name='tournament_signup'),
    path('new_player', views.new_player, name='new_player'),
    path('tournaments', views.tournaments, name='tournaments'),
    path('tournament/<int:id>/', views.tournament, name='tournament'),
    path('clubs', views.clubs, name='clubs'),
    path('ranking', views.ranking, name='ranking'),
    path('card-player', views.cardplayer, name='card-player'),
    url(r'^activate/(?P<registration_uidb64>[0-9A-Za-z_\-]+)/(?P<player_uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
