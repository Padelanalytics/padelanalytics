from django import forms

from anmeldung.models import Club
from anmeldung.models import PadelPerson
from anmeldung.models import Registration
from tournaments.models import Person


class TournamentsForm(forms.Form):
    YEAR_CHOICES = (('ALL', 'ALL'), ('2016', '2016'), ('2017', '2017'), ('2018', '2018'))
    DIVISION_CHOICES = (('ALL', 'ALL'), ('MO', 'MO'), ('WO', 'WO'), ('MXO', 'MXO'), ('M45', 'M45'), ('W40', 'W40'))
    year = forms.ChoiceField(choices=YEAR_CHOICES, initial='ALL',
                             widget=forms.Select(attrs={'onchange': 'actionform.submit();'}))
    division = forms.ChoiceField(choices=DIVISION_CHOICES, initial='ALL',
                                 widget=forms.Select(attrs={'onchange': 'actionform.submit();'}))


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = '__all__'
        exclude = ['creation_date', 'is_active_a', 'is_active_b']


def get_new_player_form(request):
    NewPlayerInlineFormSet = get_new_player_form()
    return NewPlayerInlineFormSet(request)


def get_new_player_form():
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
