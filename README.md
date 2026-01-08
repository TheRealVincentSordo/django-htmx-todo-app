# Django HTMX Todo App

A modern, responsive Todo application built with Django and HTMX. This project demonstrates how to build Single Page Application (SPA) like interfaces using standard server-side Django and a small javascript library (HTMX).

## Table of Contents
- [How it Works](#how-it-works)
- [Installation and Setup](#installation-and-setup)
- [Project Structure](#project-structure)
- [Django Basics](#django-basics)
- [HTMX Basics](#htmx-basics)
- [How to Make Updates](#how-to-make-updates)

## Installation and Setup

### Prerequisites
- Python 3.12 or higher
- pip (Python package manager)

### Steps

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/TheRealVincentSordo/django-htmx-todo-app.git
    cd django-htmx-todo-app
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run migrations:**
    ```bash
    python manage.py migrate
    ```

5.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```

6.  **Open in browser:**
    Navigate to [http://localhost:8000](http://localhost:8000) to see the app.

## How it Works

The core idea is to let Django do what it does best (render HTML) and let HTMX handle the dynamic updates.

1.  **Initial Load**: When you visit `/`, Django renders the full `index.html` page. This includes the `<head>`, implementation styles, and the initial list of todos.
2.  **Interactions**: Instead of standard HTML forms that reload the page, we use HTMX attributes (like `hx-post`).
3.  **Server Response**: When you add, toggle, or delete a todo, the server performs the database operation and returns **only the HTML for the updated list** (defined in `_todo_list.html`), not the entire page.
4.  **DOM Update**: HTMX receives this partial HTML and swaps it into the existing page (specifically, inside the `<div id="todo-list">`), creating a smooth, instant update without a full reload.

## Project Structure

```
├── config/              # Project-wide settings and configuration
│   ├── settings.py      # Main settings (installed apps, database, etc.)
│   └── urls.py          # Main URL routing
├── todos/               # The main Todo application
│   ├── models.py        # Database definition (Todo item)
│   ├── views.py         # Request handling logic
│   ├── urls.py          # App-specific URL routing
│   └── templates/       # HTML files
│       └── todos/
│           ├── index.html       # Main page
│           └── _todo_list.html  # Partial template for the list
├── db.sqlite3           # Local development database
└── manage.py            # Django command-line utility
```

## Django Basics

Django is a high-level Python web framework. Here are the key components used in this project:

### Models (`todos/models.py`)
Models define the structure of your database. Our `Todo` model has:
-   `text`: The task description.
-   `done`: A boolean (True/False) status.
-   `created_at`: Timestamp for sorting.

### Views (`todos/views.py`)
Views handle incoming requests.
-   `index`: Fetches all todos and renders the full page.
-   **Action Views** (`add_todo`, `toggle_todo`, `delete_todo`): These modify data. Crucially, they check `if request.htmx:`. If it's an HTMX request, they return the partial `_todo_list.html`. If not (e.g., standard form submit), they redirect back to the index.

### URLs (`todos/urls.py`)
This file maps browser URLs (like `/add/`) to specific Python functions in `views.py`.

## HTMX Basics

HTMX allows you to access AJAX, CSS Transitions, WebSockets and Server Sent Events directly in HTML, using attributes.

Key attributes used in this project:

-   `hx-post="{url}"`: Sends a POST request to the specified URL when the element is triggered (e.g., clicked).
-   `hx-target="#todo-list"`: Tells HTMX where to put the response. In this case, it updates the container with ID `todo-list`.
-   `hx-swap="innerHTML"`: Tells HTMX *how* to update the target. `innerHTML` replaces the content inside the target element.
-   `hx-on::after-request="this.reset()"`: A bit of Javascript to clear the input field after a successful form submission.

### Example Flow: Adding a Todo
1.  User types "Buy milk" and clicks Add.
2.  The `<form>` with `hx-post` sends the data to Django.
3.  Django creates the Todo and renders `_todo_list.html` with the new list.
4.  HTMX receives the HTML and replaces the content of `#todo-list`.

## How to Make Updates

### 1. Changing the Data Model
If you want to add a `due_date` field to your Todo:
1.  Open `todos/models.py` and add the field:
    ```python
    due_date = models.DateField(null=True, blank=True)
    ```
2.  Run migrations to update the database:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

### 2. Updating the UI
-   **Main Layout**: Edit `todos/templates/todos/index.html` for changes to the page structure, header, or global styles.
-   **List Items**: Edit `todos/templates/todos/_todo_list.html` to change how individual todos look. **Note**: Since this file is re-rendered on every update, changes here appear instantly after an action.

### 3. Adding New Features
To add a "Clear Completed" button:
1.  **View**: Add a `clear_completed` function in `todos/views.py`.
2.  **URL**: Add a path in `todos/urls.py`.
3.  **Template**: Add a button in `index.html` (or `_todo_list.html`) with `hx-post` pointing to your new URL.
