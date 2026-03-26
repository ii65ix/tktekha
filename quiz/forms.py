from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class ArenaLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = _("Username")
        self.fields["password"].label = _("Password")
        for field in self.fields.values():
            field.widget.attrs.update(
                {"class": "form-control bg-dark text-white border-secondary"}
            )


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label=_("Email address"),
        widget=forms.EmailInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        labels = {
            "username": _("Username"),
            "password1": _("Password"),
            "password2": _("Password confirmation"),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in ("username", "password1", "password2"):
            self.fields[name].widget.attrs.update({"class": "form-control"})
