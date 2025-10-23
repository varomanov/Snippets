import pprint
from django.http import Http404, HttpResponse, HttpResponseNotAllowed
from django.shortcuts import render, redirect, get_object_or_404
from .forms import SnippetForm
from .models import Snippet


def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)


def add_snippet_page(request):
    form = SnippetForm()
    context = {
        'pagename': 'Добавление нового сниппета',
        'form': form,
    }
    return render(request, 'pages/add_snippet.html', context)


def create_snippet(request):
    if request.method == 'POST':
        form = SnippetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('snippets-list')
        return render(request, 'pages/add_snippet.html', context={'form': form})

    return HttpResponseNotAllowed(['POST'], 'Only POST methods')


def snippets_page(request):
    context = {'pagename': 'Просмотр сниппетов',
               'snippets': Snippet.objects.all()}
    return render(request, 'pages/view_snippets.html', context)


def snippet_item(request, id: int):
    snippet = get_object_or_404(Snippet, id=id)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'delete':
            snippet.delete()
            return redirect('snippets-list')

        elif action == 'update':
            # Обновляем данные сниппета
            snippet.name = request.POST.get('name')
            snippet.code = request.POST.get('code')
            snippet.save()
            snippet.refresh_from_db()
            # Возвращаемся на эту же страницу
            return redirect('snippet-item', id=id)

    context = {'pagename': 'Редактирование сниппета', 'snippet': snippet}
    return render(request, 'pages/item_snippet.html', context)
