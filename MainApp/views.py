from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from MainApp.models import Snippet


def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)


def add_snippet_page(request):
    context = {'pagename': 'Добавление нового сниппета'}
    return render(request, 'pages/add_snippet.html', context)


def snippets_page(request):
    context = {'pagename': 'Просмотр сниппетов', 'snippets': Snippet.objects.all()}
    return render(request, 'pages/view_snippets.html', context)


def snippet_item(request, id: int):
    snippet = get_object_or_404(Snippet, id=id)
    context = {'pagename': 'Сниппет', 'snippet': snippet}
    return render(request, 'pages/item_snippet.html', context)


def delete_snippet(request, id: int):
    snippet = get_object_or_404(Snippet, id=id)

    # если метод POST, удаляю сниппет и перенаправляю на главную страницу
    if request.method == 'POST':
        snippet.delete()
        return redirect('/')

    # если метод GET, то просто возвращаю страницу
    return render(request, 'pages/item_snippet.html')
