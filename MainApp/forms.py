from django.forms import ModelForm, ValidationError
from .models import Snippet


class SnippetForm(ModelForm):
    class Meta:
        model = Snippet
        # описываем поля, которые будем запролнять в форме
        fields = ['name', 'lang', 'code']

    def clean_name(self):
        """Метод для проверки длины поля <name>"""
        snippet_name = self.cleaned_data.get('name')
        if snippet_name is not None and len(snippet_name):
            return snippet_name
        else:
            raise ValidationError('Name to short!')
