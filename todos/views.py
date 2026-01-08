from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import Todo


def get_stats():
    total = Todo.objects.count()
    completed = Todo.objects.filter(done=True).count()
    percent = int((completed / total * 100)) if total > 0 else 0
    return {"total": total, "completed": completed, "percent": percent}


def index(request: HttpRequest) -> HttpResponse:
    todos = Todo.objects.all()
    stats = get_stats()
    return render(request, "todos/index.html", {"todos": todos, **stats})


@require_POST
def add_todo(request: HttpRequest) -> HttpResponse:
    text = (request.POST.get("text") or "").strip()
    if text:
        Todo.objects.create(text=text)

    if request.htmx:
        stats = get_stats()
        return render(request, "todos/_todo_list.html", {"todos": Todo.objects.all(), **stats})
    return redirect("todos:index")


@require_POST
def toggle_todo(request: HttpRequest, todo_id: int) -> HttpResponse:
    todo = get_object_or_404(Todo, id=todo_id)
    todo.done = not todo.done
    todo.save(update_fields=["done"])

    if request.htmx:
        stats = get_stats()
        return render(request, "todos/_todo_list.html", {"todos": Todo.objects.all(), **stats})
    return redirect("todos:index")


@require_POST
def delete_todo(request: HttpRequest, todo_id: int) -> HttpResponse:
    todo = get_object_or_404(Todo, id=todo_id)
    todo.delete()

    if request.htmx:
        stats = get_stats()
        return render(request, "todos/_todo_list.html", {"todos": Todo.objects.all(), **stats})
    return redirect("todos:index")
    