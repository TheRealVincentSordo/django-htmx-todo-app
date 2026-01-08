from functools import wraps

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import Todo
from .middleware import SESSION_KEY
from .supabase import get_supabase_client


def supabase_login_required(view_func):
    @wraps(view_func)
    def _wrapped(request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if not getattr(request, "supabase_user", None):
            return redirect("todos:login")
        return view_func(request, *args, **kwargs)

    return _wrapped


@supabase_login_required
def index(request: HttpRequest) -> HttpResponse:
    todos = Todo.objects.filter(user_id=request.supabase_user["id"])
    return render(
        request,
        "todos/index.html",
        {"todos": todos, "supabase_user": request.supabase_user},
    )


def login(request: HttpRequest) -> HttpResponse:
    if getattr(request, "supabase_user", None):
        return redirect("todos:index")

    error = None
    if request.method == "POST":
        email = (request.POST.get("email") or "").strip()
        password = request.POST.get("password") or ""

        if not settings.SUPABASE_JWT_SECRET:
            error = "Supabase JWT secret is not configured."
        elif not email or not password:
            error = "Email and password are required."
        else:
            client = get_supabase_client()
            try:
                response = client.auth.sign_in_with_password(
                    {"email": email, "password": password}
                )
            except Exception:
                error = "Unable to sign in. Check your credentials."
            else:
                session = response.session
                if session and session.access_token:
                    request.session[SESSION_KEY] = session.access_token
                    return redirect("todos:index")
                error = "Unable to start a session."

    return render(request, "todos/login.html", {"error": error})


def logout(request: HttpRequest) -> HttpResponse:
    request.session.pop(SESSION_KEY, None)
    return redirect("todos:login")


@require_POST
@supabase_login_required
def add_todo(request: HttpRequest) -> HttpResponse:
    text = (request.POST.get("text") or "").strip()
    if text:
        Todo.objects.create(text=text, user_id=request.supabase_user["id"])

    if request.htmx:
        return render(
            request,
            "todos/_todo_list.html",
            {"todos": Todo.objects.filter(user_id=request.supabase_user["id"])},
        )
    return redirect("todos:index")


@require_POST
@supabase_login_required
def toggle_todo(request: HttpRequest, todo_id: int) -> HttpResponse:
    todo = get_object_or_404(
        Todo, id=todo_id, user_id=request.supabase_user["id"]
    )
    todo.done = not todo.done
    todo.save(update_fields=["done"])

    if request.htmx:
        return render(
            request,
            "todos/_todo_list.html",
            {"todos": Todo.objects.filter(user_id=request.supabase_user["id"])},
        )
    return redirect("todos:index")


@require_POST
@supabase_login_required
def delete_todo(request: HttpRequest, todo_id: int) -> HttpResponse:
    todo = get_object_or_404(
        Todo, id=todo_id, user_id=request.supabase_user["id"]
    )
    todo.delete()

    if request.htmx:
        return render(
            request,
            "todos/_todo_list.html",
            {"todos": Todo.objects.filter(user_id=request.supabase_user["id"])},
        )
    return redirect("todos:index")
