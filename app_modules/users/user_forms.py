from django import forms
from django.contrib.auth import get_user_model
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox

User = get_user_model()

class UserForm(forms.ModelForm):
    
    """User Create Form"""
    
    role = forms.ChoiceField(choices=User.USER_ROLE, required=False, label="Role")
    captcha = ReCaptchaField(
        widget=ReCaptchaV2Checkbox,
        error_messages={
            'required': 'Please complete the CAPTCHA to proceed.',
            'invalid': 'The CAPTCHA is invalid, please try again.'
        }
    )
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "mobile",
            "email",
            "image",
            "username",
            "captcha",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['image'].required = True if not self.instance.pk else False
        if self.instance.pk:
            self.fields['username'].disabled = True