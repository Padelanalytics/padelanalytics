from django import forms
from django.utils.translation import gettext_lazy as _

from anmeldung.models import PadelPerson, Registration
from tournaments.models import (
    PADEL_DIVISION_GERMANY,
    PADEL_DIVISION_SWITZERLAND,
    PADEL_DIVISION_THAILAND,
    PADEL_DIVISION_WPT,
    Club,
    PadelRanking,
    Person,
    get_last_ranking_date,
    get_padel_ranking_default_division,
)
from tournaments.helpers import all_mondays_from_to

INTERNATIONAL_YEAR_CHOICES = (("ALL", _("ALL")), ("2019", "2019"))
GER_YEAR_CHOICES = (
    ("ALL", _("ALL")),
    ("2020", "2020"),
    ("2019", "2019"),
    ("2018", "2018"),
    ("2017", "2017"),
    ("2016", "2016"),
)
WPT_YEAR_CHOICES = (
    ("ALL", _("ALL")),
    ("2020", "2020"),
    ("2019", "2019"),
    ("2018", "2018"),
)
NED_YEAR_CHOICES = (
    ("ALL", _("ALL")),
    ("2020", "2020"),
    ("2019", "2019"),
    ("2018", "2018"),
)
THA_YEAR_CHOICES = (("ALL", _("ALL")), ("2019", "2019"))
PADEL_RANKING_DIVISION_NETHERLANDS = (
    ("MO", _("Men")),
    ("WO", _("Women")),
)


def get_divisions(federation):
    fed = federation.upper()
    if fed == "GERMANY":
        div_choices = PADEL_DIVISION_GERMANY
    elif fed == "THAILAND":
        div_choices = PADEL_DIVISION_THAILAND
    elif fed == "SWITZERLAND":
        div_choices = PADEL_DIVISION_SWITZERLAND
    elif fed == "WPT":
        div_choices = PADEL_DIVISION_WPT
    elif fed == "NETHERLANDS":
        div_choices = PADEL_RANKING_DIVISION_NETHERLANDS
    elif fed == "INTERNATIONAL":
        div_choices = PADEL_RANKING_DIVISION_NETHERLANDS
    else:
        raise ValueError("Federation not supported.")
    return div_choices


def get_years(federation):
    fed = federation.upper()
    if fed == "GERMANY":
        years = GER_YEAR_CHOICES
    elif fed == "THAILAND":
        years = THA_YEAR_CHOICES
    elif fed == "NETHERLANDS":
        years = NED_YEAR_CHOICES
    elif fed == "WPT":
        years = WPT_YEAR_CHOICES
    elif fed == "INTERNATIONAL":
        years = INTERNATIONAL_YEAR_CHOICES
    else:
        raise ValueError("Federation not supported.")
    return years


class RankingForm(forms.Form):
    def __init__(self, *args, **kwargs):
        federation = kwargs.pop("federation")
        circuit = kwargs.pop("circuit")
        super().__init__(*args, **kwargs)
        last_ranking_date = get_last_ranking_date(federation, circuit)
        division = self.data.get("division")

        if division is None:
            division = get_padel_ranking_default_division(federation)

        rankings = PadelRanking.objects.filter(
            country=federation, division=division, date__lte=last_ranking_date
        ).order_by("date")

        try:
            # set form initial division and choices
            div_choices = get_divisions(federation)
            self.fields["division"].choices = div_choices
            self.fields["division"].initial = div_choices[0]

            # set form initial date and choices
            date_choices = all_mondays_from_to(rankings.first().date, last_ranking_date, True)
            date_choices.reverse()
            self.fields["date"].choices = date_choices
            self.fields["date"].initial = date_choices[0]
        except Exception:
            self.fields["date"].choices = None

    date = forms.ChoiceField(
        widget=forms.Select(
            attrs={"onchange": "$(\"form[name='ranking-form']\")[0].submit();"}
        )
    )

    division = forms.ChoiceField(
        widget=forms.Select(
            attrs={"onchange": "$(\"form[name='ranking-form']\")[0].submit();"}
        )
    )


class TournamentsForm(forms.Form):
    def __init__(self, *args, **kwargs):
        federation = kwargs.pop("federation")
        super().__init__(*args, **kwargs)

        # available years
        years = get_years(federation)
        self.fields["year"].choices = years
        self.fields["year"].initial = years[0]
        # available divisions
        divisions = get_divisions(federation)
        divisions = (("ALL", _("ALL")),) + divisions
        self.fields["division"].choices = divisions
        self.fields["division"].initial = divisions[0]

    year = forms.ChoiceField(
        widget=forms.Select(
            attrs={"onchange": "$(\"form[name='tournaments-form']\")[0].submit();"}
        )
    )

    division = forms.ChoiceField(
        widget=forms.Select(
            attrs={"onchange": "$(\"form[name='tournaments-form']\")[0].submit();"}
        )
    )


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = "__all__"
        exclude = ["creation_date", "is_active_a", "is_active_b"]


class SearchForm(forms.Form):
    text = forms.CharField(
        label="Search",
        required=True,
        max_length=40,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Search players, teams, cities, tournaments...",
            }
        ),
    )


def get_new_player_form(request):
    NewPlayerInlineFormSet = get_new_player_form_()
    return NewPlayerInlineFormSet(request)


def get_new_player_form_():
    GENDER_CHOICES = (("M", "Male"), ("F", "Female"))

    NewPlayerInlineFormSet = forms.inlineformset_factory(
        Person,
        PadelPerson,
        exclude=["ranking_points", "photo"],
        widgets={
            "email": forms.EmailInput(attrs={"placeholder": "Mail-Adresse"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Familienname"}),
            "last_name2": forms.TextInput(attrs={"placeholder": "Familienname 2"}),
            "first_name": forms.TextInput(attrs={"placeholder": "Vorname"}),
            "gender": forms.Select(
                choices=GENDER_CHOICES, attrs={"placeholder": "Geschlecht"}
            ),
            "phone": forms.TextInput(attrs={"placeholder": "Telefonnummer"}),
            "city": forms.TextInput(attrs={"placeholder": "Wohnort"}),
            "club": forms.Select(choices=Club.objects.all(), attrs={"placeholder": "Verein"}),
            "birthplace": forms.TextInput(attrs={"placeholder": "Geburtsort"}),
            "born": forms.DateInput(format="%Y-%m-%d", attrs={"placeholder": "Geburtsdatum"}),
            "country": forms.Select(attrs={"placeholder": "Land"}),
            "policy_read_a": forms.CheckboxInput(attrs={"placeholder": "Accept"}),
            "policy_read_b": forms.CheckboxInput(attrs={"placeholder": "Accept"}),
            "policy_read_c": forms.CheckboxInput(attrs={"placeholder": "Accept"}),
        },
    )
    return NewPlayerInlineFormSet
