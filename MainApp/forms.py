from django.forms import ModelForm, ValidationError, Textarea, TextInput
from .models import Snippet


class SnippetForm(ModelForm):
    class Meta:
        model = Snippet
        # описываем поля, которые будем запролнять в форме
        fields = ['name', 'lang', 'code', 'is_private']
        labels = {'name': '', 'lang': '', 'code': '', 'is_private': ''}
        widgets = {
            'name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название спиннета',
                'style': 'max-width: 300px'
            }),
            'code': Textarea(attrs={
                'placeholder': 'Код сниппета',
                'rows': 5,
                'class': 'input-large',
                'style': 'width: 50% ! important; resize: vertical !important;'
            })
        }

    def clean_name(self):
        """Метод для проверки длины поля <name>"""
        snippet_name = self.cleaned_data.get('name')
        if snippet_name is not None and len(snippet_name) > 3:
            return snippet_name
        else:
            raise ValidationError('Name to short!')
