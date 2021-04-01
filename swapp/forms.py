from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


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
