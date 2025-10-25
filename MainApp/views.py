import pprint
from django.http import Http404, HttpResponse, HttpResponseNotAllowed
from django.shortcuts import render, redirect, get_object_or_404
from .forms import SnippetForm
from .models import Snippet
from django.contrib import auth
from django.db.models import Q


def index_page(request):
    if request.user.is_authenticated:
        snippets = Snippet.objects.filter(user=request.user)
        context = {"pagename": "PythonBin", "snippets": snippets}
        return render(request, "pages/index.html", context)
    return render(request, "pages/index.html")


def add_snippet_page(request):
    # при ГЕТ методе формируется путая форма
    if request.method == "GET":
        form = SnippetForm()
        context = {
            "pagename": "Добавление нового сниппета",
            "form": form,
        }
        return render(request, "pages/add_snippet.html", context)

    # Получаем данные из формыи и на их основе создаем новый сниппет, сохраняя его в БД
    if request.method == "POST":
        form = SnippetForm(request.POST)
    if form.is_valid:
        snippet = form.save(commit=False)  # получаем экземпляр класса Snippet
    if request.user.is_authenticated:
        snippet.user = request.user
        snippet.save()
        # GET /snippets/list
        return redirect("snippets-list")  # URL для списка сниппитов
    return render(request, "pages/add_snippet.html", context={"form": form})


def snippets_auth(request):
    context = {"pagename": "Просмотр сниппетов"}
    snippets = Snippet.objects.filter(user=request.user)
    context["snippets"] = snippets
    return render(request, "pages/view_snippets_auth.html", context)


def snippets_page(request):
    context = {"pagename": "Просмотр сниппетов"}
    if request.user.is_authenticated:
        context["snippets"] = Snippet.objects.filter(Q(is_private=0) | Q(user=request.user))
    else:
        context["snippets"] = Snippet.objects.filter(is_private=0)
    return render(request, "pages/view_snippets.html", context)


def snippet_item(request, id: int):
    snippet = get_object_or_404(Snippet, id=id)

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "delete":
            snippet.delete()
            return redirect("snippets-list")

        elif action == "update":
            # Обновляем данные сниппета
            snippet.name = request.POST.get("name")
            snippet.code = request.POST.get("code")
            snippet.save()
            snippet.refresh_from_db()
            # Возвращаемся на эту же страницу
            return redirect("snippet-item", id=id)

    context = {"pagename": "Редактирование сниппета", "snippet": snippet}
    return render(request, "pages/item_snippet.html", context)


def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            print(user)
        else:
            print(user)
            pass
    return redirect("home")


def logout(request):
    auth.logout(request)
    return redirect("home")
