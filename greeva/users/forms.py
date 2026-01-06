from allauth.account.forms import SignupForm, LoginForm
from allauth.socialaccount.forms import SignupForm as SocialSignupForm
from django.contrib.auth import forms as admin_forms
from django.forms import EmailField
from django.utils.translation import gettext_lazy as _

from .models import User


class UserAdminChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):  # type: ignore[name-defined]
        model = User
        field_classes = {"email": EmailField}


class UserAdminCreationForm(admin_forms.UserCreationForm):
    """
    Form for User Creation in the Admin Area.
    To change user signup, see UserSignupForm and UserSocialSignupForm.
    """

    class Meta(admin_forms.UserCreationForm.Meta):  # type: ignore[name-defined]
        model = User
        fields = ("email",)
        field_classes = {"email": EmailField}
        error_messages = {
            "email": {"unique": _("This email has already been taken.")},
        }


class UserSignupForm(SignupForm):
    """
    Form that will be rendered on a user sign up section/screen.
    Default fields will be added automatically.
    Check UserSocialSignupForm for accounts created from social.
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add autocomplete attributes for proper browser behavior
        if 'email' in self.fields:
            self.fields['email'].widget.attrs['autocomplete'] = 'email'
        if 'password1' in self.fields:
            self.fields['password1'].widget.attrs['autocomplete'] = 'new-password'
        if 'password2' in self.fields:
            self.fields['password2'].widget.attrs['autocomplete'] = 'new-password'


class UserSocialSignupForm(SocialSignupForm):
    """
    Renders the form when user has signed up using social accounts.
    Default fields will be added automatically.
    See UserSignupForm otherwise.
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add autocomplete attributes for proper browser behavior
        if 'email' in self.fields:
            self.fields['email'].widget.attrs['autocomplete'] = 'email'


class UserLoginForm(LoginForm):
    """
    Custom login form with proper autocomplete attributes.
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add autocomplete attributes for proper browser behavior
        if 'login' in self.fields:
            self.fields['login'].widget.attrs['autocomplete'] = 'email'
        if 'password' in self.fields:
            self.fields['password'].widget.attrs['autocomplete'] = 'current-password'
