import datetime
from django import forms
from django.utils.translation import gettext_lazy as _

from anmeldung.models import PadelPerson, Registration
from tournaments.models import PADEL_DIVISION_CHOICES, PADEL_DIVISION_CHOICES_ALL, Club, Person, PadelRanking, get_padel_ranking_default_division
from tournaments.service import all_mondays_from_to


class RankingForm(forms.Form):
    def __init__(self, *args, **kwargs):
        federation = kwargs.pop('federation')
        super().__init__(*args, **kwargs)
        division = self.data.get('division') or get_padel_ranking_default_division(federation)
        last_ranking_date = datetime.date(2019, 9, 9)
        rankings = PadelRanking.objects.filter(
            country=federation,
            division=division,
            date__lte=last_ranking_date).order_by('date')

        if rankings:
            choices = all_mondays_from_to(
                rankings.first().date,
                last_ranking_date,
                True)
            choices.reverse()
            self.fields['date'].choices = choices
            self.fields['date'].initial = choices[0]

    date = forms.ChoiceField(
        widget=forms.Select(
            attrs={
                'onchange': "$(\"form[name='ranking-form']\")[0].submit();"}))

    division = forms.ChoiceField(
        choices=PADEL_DIVISION_CHOICES,
        initial=_('MO'),
        widget=forms.Select(attrs={
            'onchange': "$(\"form[name='ranking-form']\")[0].submit();"}))


class TournamentsForm(forms.Form):
    YEAR_CHOICES = (('ALL', _('ALL')), ('2019', '2019'), ('2018', '2018'), ('2017', '2017'), ('2016', '2016'))

    year = forms.ChoiceField(
        choices=YEAR_CHOICES,
        initial=_('ALL'),
        widget=forms.Select(attrs={'onchange': "$(\"form[name='tournamets-form']\")[0].submit();"}))

    division = forms.ChoiceField(
        choices=PADEL_DIVISION_CHOICES_ALL,
        initial=_('ALL'),
        widget=forms.Select(attrs={'onchange': "$(\"form[name='tournamets-form']\")[0].submit();"}))


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = '__all__'
        exclude = ['creation_date', 'is_active_a', 'is_active_b']


class SearchForm(forms.Form):
    text = forms.CharField(
        label='Search',
        required=True,
        max_length=40,
        widget=forms.TextInput(attrs={'class': 'form-control',
         'placeholder': 'Search players, teams, cities, tournaments...'}))


def get_new_player_form(request):
    NewPlayerInlineFormSet = get_new_player_form_()
    return NewPlayerInlineFormSet(request)


def get_new_player_form_():
    GENDER_CHOICES = (('M', 'Male'), ('F', 'Female'))

    NewPlayerInlineFormSet = forms.inlineformset_factory(
        Person,
        PadelPerson,
        exclude=['ranking_points', 'photo'],
        widgets={
            'email': forms.EmailInput(attrs={'placeholder': 'Mail-Adresse'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Familienname'}),
            'last_name2': forms.TextInput(attrs={'placeholder': 'Familienname 2'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Vorname'}),
            'gender': forms.Select(choices=GENDER_CHOICES, attrs={'placeholder': 'Geschlecht'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Telefonnummer'}),
            'city': forms.TextInput(attrs={'placeholder': 'Wohnort'}),
            'club': forms.Select(choices=Club.objects.all(), attrs={'placeholder': 'Verein'}),
            'birthplace': forms.TextInput(attrs={'placeholder': 'Geburtsort'}),
            'born': forms.DateInput(format='%Y-%m-%d', attrs={'placeholder': 'Geburtsdatum'}),
            'country': forms.Select(attrs={'placeholder': 'Land'}),
            'policy_read_a': forms.CheckboxInput(attrs={'placeholder': 'Accept'}),
            'policy_read_b': forms.CheckboxInput(attrs={'placeholder': 'Accept'}),
            'policy_read_c': forms.CheckboxInput(attrs={'placeholder': 'Accept'})
        }
    )
    return NewPlayerInlineFormSet
