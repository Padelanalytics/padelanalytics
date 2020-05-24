from django import forms
from django.utils.translation import gettext_lazy as _

from anmeldung.models import PadelPerson, Registration
from tournaments.models import PADEL_DIVISION_CHOICES_ALL
from tournaments.models import PADEL_DIVISION_GERMANY
from tournaments.models import PADEL_DIVISION_NETHERLANDS
from tournaments.models import PADEL_DIVISION_THAILAND
from tournaments.models import PADEL_DIVISION_SWITZERLAND
from tournaments.models import PADEL_DIVISION_WPT
from tournaments.models import Club, Person, PadelRanking
from tournaments.models import get_padel_ranking_default_division
from tournaments.models import get_last_ranking_date
from tournaments.service import all_mondays_from_to


GER_YEAR_CHOICES = (('ALL', _('ALL')), ('2020', '2020'), ('2019', '2019'), ('2018', '2018'), ('2017', '2017'), ('2016', '2016'))
WPT_YEAR_CHOICES = (('ALL', _('ALL')), ('2020', '2020'), ('2019', '2019'), ('2018', '2018'))
NED_YEAR_CHOICES = (('ALL', _('ALL')), ('2020', '2020'), ('2019', '2019'), ('2018', '2018'))
THA_YEAR_CHOICES = (('ALL', _('ALL')), ('2019', '2019'))


def get_divisions(federation):
    if federation == "Germany":
        div_choices = (('ALL', _('ALL')), ) + PADEL_DIVISION_GERMANY
    elif federation == "Thailand":
        div_choices = (('ALL', _('ALL')), ) + PADEL_DIVISION_THAILAND
    elif federation == "Switzerland":
        div_choices = (('ALL', _('ALL')), ) + PADEL_DIVISION_SWITZERLAND
    elif federation == "WPT":
        div_choices = (('ALL', _('ALL')), ) + PADEL_DIVISION_WPT
    elif federation == "Netherlands":
        div_choices = (('ALL', _('ALL')), ) + PADEL_DIVISION_NETHERLANDS
    else:
        raise ValueError("Country not supported.")
    return div_choices


def get_years(federation):
    if federation == "Germany":
        years = GER_YEAR_CHOICES
    elif federation == "Thailand":
        years = THA_YEAR_CHOICES
    elif federation == "Netherlands":
        years = NED_YEAR_CHOICES
    elif federation == "WPT":
        years = WPT_YEAR_CHOICES
    else:
        raise ValueError("Country not supported.")
    return years


class RankingForm(forms.Form):

    def __init__(self, *args, **kwargs):
        federation = kwargs.pop('federation')
        super().__init__(*args, **kwargs)
        last_ranking_date = get_last_ranking_date()
        division = self.data.get('division')

        if division is None:
            division = get_padel_ranking_default_division(federation)

        rankings = PadelRanking.objects.filter(
            country=federation,
            division=division,
            date__lte=last_ranking_date).order_by('date')

        try:
            # set form initial division and choices
            div_choices = get_divisions(federation)
            self.fields['division'].choices = div_choices
            self.fields['division'].initial = div_choices[0]

            # set form initial date and choices
            date_choices = all_mondays_from_to(
                rankings.first().date,
                last_ranking_date,
                True)
            date_choices.reverse()
            self.fields['date'].choices = date_choices
            self.fields['date'].initial = date_choices[0]
        except Exception:
            self.fields['date'].choices = None

    date = forms.ChoiceField(
        widget=forms.Select(
            attrs={
                'onchange': "$(\"form[name='ranking-form']\")[0].submit();"}))

    division = forms.ChoiceField(
        widget=forms.Select(attrs={
            'onchange': "$(\"form[name='ranking-form']\")[0].submit();"}))


class TournamentsForm(forms.Form):

    def __init__(self, *args, **kwargs):
        federation = kwargs.pop('federation')
        super().__init__(*args, **kwargs)

        # available years
        years = get_years(federation)
        self.fields['year'].choices = years
        self.fields['year'].initial = years[0]
        # available divisions
        divisions = get_divisions(federation)
        self.fields['division'].choices = divisions
        self.fields['division'].initial = divisions[0]

    year = forms.ChoiceField(
        widget=forms.Select(
            attrs={
                'onchange': "$(\"form[name='tournaments-form']\")[0].submit();"}))

    division = forms.ChoiceField(
        widget=forms.Select(attrs={
            'onchange': "$(\"form[name='tournaments-form']\")[0].submit();"}))


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
