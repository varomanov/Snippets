from django.forms import ModelForm, Textarea, TextInput, CharField, PasswordInput
from .models import Snippet
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class SnippetForm(ModelForm):
    class Meta:
        model = Snippet
        # описываем поля, которые будем запролнять в форме
        fields = ["name", "lang", "code", "is_private"]
        labels = {"name": "", "lang": "", "code": "", "is_private": ""}
        widgets = {
            "name": TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Название спиннета",
                    "style": "max-width: 300px",
                }
            ),
            "code": Textarea(
                attrs={
                    "placeholder": "Код сниппета",
                    "rows": 5,
                    "class": "input-large",
                    "style": "width: 50% ! important; resize: vertical !important;",
                }
            ),
        }

    def clean_name(self):
        """Метод для проверки длины поля <name>"""
        snippet_name = self.cleaned_data.get("name")
        if snippet_name is not None and len(snippet_name) > 3:
            return snippet_name
        else:
            raise ValidationError("Name to short!")


class UserRegistrationForm(ModelForm):
    class Meta:
        model = User
        fields = ["username", "email"]

    password1 = CharField(label="password", widget=PasswordInput)
    password2 = CharField(label="password confirm", widget=PasswordInput)

    def clean_password2(self):
        pass1 = self.cleaned_data.get("password1")
        pass2 = self.cleaned_data.get("password2")
        if pass1 and pass2 and pass1 == pass2:
            return pass2
        raise ValidationError("Пароли не совпадают или пустые")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
