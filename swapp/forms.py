from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils import timezone
from swapp import models
from swapp.models import Event


class UserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                "The username '%(username)s' already exists.",
                params={"username": username},
                code='unique',
            )
        return username

    def clean(self):
        now = timezone.now()
        current_event = Event.objects.get(pk=1)
        seller_count = User.objects.filter(groups__name__contains='Seller').count()
        if now < current_event.registration_start_time:
            raise forms.ValidationError(
                "Registration has not started yet, come back %(start)s",
                params={"start": current_event.registration_start_time},
                code='early',
            )
        elif now > current_event.registration_end_time:
            raise forms.ValidationError(
                "Registration has already ended, deadline was %(end)s",
                params={"end": current_event.registration_end_time},
                code='late',
            )
        elif seller_count >= current_event.seller_cap:
            raise forms.ValidationError(
                "Sorry, no more registrations are allowed for this event at the moment.", code='exceeded')

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

    def clean_registration_start_time(self):
        registration_start_time = self.cleaned_data.get("registration_start_time")
        current_event = Event.objects.get(pk=1)
        if registration_start_time > current_event.end_time:
            raise forms.ValidationError(
                "Registration can't start after the event ends (%(end)s)",
                params={"end": current_event.end_time},
                code='late',
            )
        elif registration_start_time > current_event.registration_end_time:
            raise forms.ValidationError(
                "Registration can't start after it ends (%(end)s)",
                params={"end": current_event.registration_end_time},
                code='late',
            )
        return registration_start_time


class RegistrationEndTimeForm(forms.ModelForm):

    class Meta:
        model = models.Event
        fields = {"registration_end_time"}

    def clean_registration_end_time(self):
        registration_end_time = self.cleaned_data.get("registration_end_time")
        current_event = Event.objects.get(pk=1)
        if registration_end_time < current_event.registration_start_time:
            raise forms.ValidationError(
                "Registration can't end before it starts (%(start)s)",
                params={"start": current_event.registration_start_time},
                code='early',
            )
        return registration_end_time


class EventStartTimeForm(forms.ModelForm):

    class Meta:
        model = models.Event
        fields = {"start_time"}

    def clean_start_time(self):
        start_time = self.cleaned_data.get("start_time")
        current_event = Event.objects.get(pk=1)
        if start_time > current_event.end_time:
            raise forms.ValidationError(
                "Event can't start after it ends (%(end)s)",
                params={"end": current_event.end_time},
                code='late',
            )
        return start_time


class EventEndTimeForm(forms.ModelForm):

    class Meta:
        model = models.Event
        fields = {"end_time"}

    def clean_end_time(self):
        end_time = self.cleaned_data.get("end_time")
        current_event = Event.objects.get(pk=1)
        if end_time < current_event.start_time:
            raise forms.ValidationError(
                "Event can't end before it starts (%(start)s)",
                params={"start": current_event.start_time},
                code='late',
            )
        return end_time


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

    def clean_seller_cap(self):
        cap = self.cleaned_data.get('seller_cap')
        current_seller_count = User.objects.filter(groups__name__contains='Seller').count()
        if cap < current_seller_count:
            raise forms.ValidationError(
                "The seller cap can't be lower than the current number of registered Sellers (%(count)s)",
                params={"count": current_seller_count},
                code="low")
        return cap


class ItemForm(forms.ModelForm):

    class Meta:
        model = models.Item
        fields = ["name", "picture", "description", "price"]
        widgets = {
            "description": forms.Textarea(attrs={"cols": 40, "rows": 5})
        }

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price < 0.0:
            raise forms.ValidationError(
                "Price has to be a positive number",
                code="negative"
            )
        elif price > models.Item.MAX_PRICE:
            raise forms.ValidationError(
                "The price is too high. Maximum supported price is %(max_price)s",
                params={"max_price": models.Item.MAX_PRICE},
                code="overflow"
            )
        return price
