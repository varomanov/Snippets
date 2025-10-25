from django.db import models
from django.contrib.auth.models import User


LANGS = (
    ('py', 'Python'),
    ('js', 'JavaScript'),
    ('go', 'Golang'),
    ('cpp', 'C++'),
    ('html', 'HTML'),
)

IS_PRIVATE = (
    (True, 'Private'),
    (False, 'Public')
)

class Snippet(models.Model):
    name = models.CharField(max_length=100)
    lang = models.CharField(max_length=30, choices=LANGS)
    code = models.TextField(max_length=5000)
    creation_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True)
    is_private = models.BooleanField(choices=IS_PRIVATE, blank=True, null=True)
