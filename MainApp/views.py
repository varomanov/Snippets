import pprint
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from MainApp.models import Snippet


def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)


def add_snippet_page(request):
    if request.method == 'POST':
        name = request.POST['name']
        lang = request.POST['lang']
        code = request.POST['code']
        Snippet.objects.create(name=name, lang=lang, code=code).save()
        return redirect('snippets-list')

    context = {'pagename': 'Добавление нового сниппета'}
    return render(request, 'pages/add_snippet.html', context)


def snippets_page(request):
    context = {'pagename': 'Просмотр сниппетов', 'snippets': Snippet.objects.all()}
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
            return redirect('snippet-item', id=id)  # Возвращаемся на эту же страницу

    context = {'pagename': 'Редактирование сниппета', 'snippet': snippet}
    return render(request, 'pages/item_snippet.html', context)
