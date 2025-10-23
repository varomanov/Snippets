from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from MainApp import views

urlpatterns = [
    path('', views.index_page, name='home'),
    path('snippets/add', views.add_snippet_page, name='snippets-add'),
    path('snippets/list', views.snippets_page, name='snippets-list'),
    path('snippets/<int:id>', views.snippet_item, name='snippet-item'),
    path('snippets/create', views.create_snippet, name='create-snippet')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)