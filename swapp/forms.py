from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from swapp import models


class UserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2', )

class AnnouncementForm(forms.ModelForm):
    # prefix = "ann-form"

    class Meta:
        model = models.Announcement
        fields = ['title', 'announcement', 'picture']
        widgets = {
            "announcement": forms.Textarea(attrs={"cols": 40, "rows": 5})
        }



class RegistrationStartTimeForm(forms.ModelForm):

    class Meta:
        model = models.Event
        fields = {"registration_start_time"}


class RegistrationEndTimeForm(forms.ModelForm):

    class Meta:
        model = models.Event
        fields = {"registration_end_time"}


class EventStartTimeForm(forms.ModelForm):

    class Meta:
        model = models.Event
        fields = {"start_time"}


class EventEndTimeForm(forms.ModelForm):

    class Meta:
        model = models.Event
        fields = {"end_time"}


class EventLocationForm(forms.ModelForm):

    class Meta:
        model = models.Event
        fields = {"location"}


class EventDescriptionForm(forms.ModelForm):

    class Meta:
        model = models.Event
        fields = {"description"}
        widgets = {
            "description": forms.Textarea(attrs={"cols": 40, "rows": 5})
        }


class RegistrationCapForm(forms.ModelForm):

    class Meta:
        model = models.Event
        fields = {"seller_cap"}
