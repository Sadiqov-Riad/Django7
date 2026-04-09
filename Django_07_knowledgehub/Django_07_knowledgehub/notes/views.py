from django.http import HttpResponse, HttpRequest
from django.middleware.csrf import get_token
from django.shortcuts import redirect
from django.utils.html import escape
from django.urls import reverse

from notes import data


# Create your views here.

def _html_shell(title: str, body: str) -> str:
    safe_title = escape(title)
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{safe_title}</title>

    <link
        href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
        rel="stylesheet"
    >

    <style>
        :root {{
            --bg-1: #f4f7fb;
            --bg-2: #eaf1fb;
            --surface: #ffffff;
            --surface-soft: #f7f9fc;
            --text: #1f2937;
            --muted: #6b7280;
            --accent: #0f5cc0;
            --accent-2: #2a7be8;
            --danger: #c62828;
            --radius: 18px;
        }}

        body {{
            color: var(--text);
            background:
                radial-gradient(circle at 10% 10%, rgba(42, 123, 232, 0.08), transparent 36%),
                radial-gradient(circle at 90% 0%, rgba(15, 92, 192, 0.08), transparent 30%),
                linear-gradient(145deg, var(--bg-1), var(--bg-2));
            min-height: 100vh;
        }}

        .top-nav {{
            background: rgba(12, 33, 67, 0.93);
            backdrop-filter: blur(8px);
        }}

        .navbar-brand {{
            font-weight: 600;
            letter-spacing: 0.3px;
        }}

        .main-card {{
            border: 0;
            border-radius: var(--radius);
            background: var(--surface);
            box-shadow: 0 14px 40px rgba(15, 23, 42, 0.1);
        }}

        .page-title {{
            font-weight: 650;
            letter-spacing: -0.02em;
            margin-bottom: 0.3rem;
        }}

        .page-subtitle {{
            color: var(--muted);
            margin-bottom: 1.25rem;
        }}

        .info-pill {{
            display: inline-block;
            padding: 0.25rem 0.65rem;
            font-size: 0.78rem;
            border-radius: 999px;
            background: #edf2fa;
            color: #2c3e57;
            margin-right: 0.35rem;
        }}

        footer {{
            color: var(--muted);
            font-size: 0.92rem;
        }}

        .btn-primary {{
            background: var(--accent);
            border-color: var(--accent);
        }}

        .btn-primary:hover {{
            background: var(--accent-2);
            border-color: var(--accent-2);
        }}

        .btn-danger {{
            background: var(--danger);
            border-color: var(--danger);
        }}

        .form-control {{
            border-radius: 12px;
            border-color: #d3dbe7;
            padding: 0.65rem 0.8rem;
        }}

        .form-control:focus {{
            border-color: #7cadf1;
            box-shadow: 0 0 0 0.2rem rgba(42, 123, 232, 0.16);
        }}

        textarea.form-control {{
            min-height: 140px;
            resize: vertical;
        }}

        .list-group-item {{
            border-left: 0;
            border-right: 0;
            padding: 1rem 0.5rem;
            background: transparent;
        }}

        .list-group-item:first-child {{
            border-top: 0;
        }}

        .note-title-link {{
            color: #1d4f94;
            text-decoration: none;
            font-weight: 600;
        }}

        .note-title-link:hover {{
            color: #0d3c75;
            text-decoration: underline;
        }}

        .actions-row {{
            display: flex;
            gap: 0.6rem;
            flex-wrap: wrap;
            align-items: center;
        }}

        .muted {{
            color: var(--muted);
        }}
    </style>
</head>
<body>

    <nav class="navbar navbar-expand-lg navbar-dark top-nav shadow-sm">
        <div class="container">
            <a class="navbar-brand" href="{escape(reverse('home'))}">Knowledge Hub</a>

            <button
                class="navbar-toggler"
                type="button"
                data-bs-toggle="collapse"
                data-bs-target="#mainNavbar"
                aria-controls="mainNavbar"
                aria-expanded="false"
                aria-label="Toggle navigation"
            >
                <span class="navbar-toggler-icon"></span>
            </button>

            <div class="collapse navbar-collapse" id="mainNavbar">
                <ul class="navbar-nav ms-auto mb-2 mb-lg-0">
                    <li class="nav-item">
                        <a class="nav-link" href="{escape(reverse('home'))}">Home</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{escape(reverse('about'))}">About</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{escape(reverse('notes_list'))}">Notes</a>
                    </li>
                     <li class="nav-item">
                        <a class="nav-link" href="{escape(reverse('note_create'))}">New note</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <main class="container py-5">
        <div class="card main-card">
            <div class="card-body p-4 p-md-5">
                {body}
            </div>
        </div>
    </main>

    <footer class="text-center py-4">
        <div class="container">
            <span>Powered by Nadir Zamanov</span>
        </div>
    </footer>

    <script
        src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js">
    </script>
</body>
</html>
"""


def _csrf_field(request: HttpRequest) -> str:
    token = get_token(request)
    return f'<input type="hidden" name="csrfmiddlewaretoken" value="{escape(token)}">'


def home(request: HttpRequest) -> HttpResponse:
    body = f"""
    <div class="mx-auto" style="max-width: 680px;">
        <h1 class="page-title">Knowledge Hub</h1>
        <p class="page-subtitle">A clean place to store and review your technical notes.</p>

        <div class="p-4 rounded-4" style="background: #f7f9fd; border: 1px solid #e4ebf7;">
            <p class="mb-3 muted">Use quick actions to create a note or browse existing notes.</p>

            <div class="actions-row">
                <a href="{escape(reverse('notes_list'))}" class="btn btn-primary">Open notes</a>
                <a href="{escape(reverse('note_create'))}" class="btn btn-outline-primary">Create note</a>
            </div>
        </div>
    </div>
"""
    return HttpResponse(_html_shell("Knowledge Hub - Home", body))

def about(request: HttpRequest) -> HttpResponse:
    body = f"""
    <div class="mx-auto" style="max-width: 680px;">
        <h1 class="page-title">About</h1>
        <p class="page-subtitle">Training project for Django course practice.</p>

        <div class="p-4 rounded-4" style="background: #f7f9fd; border: 1px solid #e4ebf7;">
            <p class="mb-2"><strong>Module:</strong> Lesson 7</p>
            <p class="mb-0 muted">Focus: routes, views, forms and CRUD actions.</p>
        </div>
    </div>
"""
    return HttpResponse(_html_shell("Knowledge Hub - About", body))


def notes_list(request: HttpRequest) -> HttpResponse:
    raw_tag = request.GET.get("tag")
    raw_category = request.GET.get("category")

    notes = data.list_notes()

    if raw_tag:
        tag_filter = raw_tag.strip().lower()
        notes = [n for n in notes if n["tag"].lower() == tag_filter]

    if raw_category:
        category_filter = raw_category.strip().lower()
        notes = [n for n in notes if n["category"].lower() == category_filter]

    items: list[str] = []
    for note in notes:
        url = reverse("note_detail", kwargs={"note_id": note["id"]})
        items.append(f"""
        <li class="list-group-item">

            <a href="{escape(url)}" class="note-title-link">
                {escape(note['title'])}
            </a>

            <div class="small muted mt-2">
                <span class="info-pill">Tag: {escape(note['tag'])}</span>
                <span class="info-pill">Category: {escape(note['category'])}</span>
            </div>

        </li>
""")

    items_html = "\n".join(items)
    if not items_html:
        items_html = '<li class="list-group-item muted">No notes found.</li>'

    filter_hint = f"""
        <p class="muted mb-3">Filter examples:
        <a href="?tag=python">?tag=python</a> |
        <a href="?category=backend">?category=backend</a> |
        <a href="{escape(reverse('notes_list'))}">Reset</a>
        </p>
    """

    body = f"""
    <div class="mx-auto" style="max-width: 760px;">

        <h1 class="page-title">Notes</h1>
        <p class="page-subtitle">Browse and manage all saved notes.</p>

        {filter_hint}

        <ul class="list-group list-group-flush">
            {items_html}
        </ul>

        <div class="mt-4">
            <a href="{escape(reverse('note_create'))}" class="btn btn-primary">Create note</a>
        </div>
    </div>
    """

    return HttpResponse(_html_shell("Notes list", body))


def note_detail(request: HttpRequest, note_id: int) -> HttpResponse:
    note = data.get_note(note_id)
    if note is None:
        body = f"""
    <div class="mx-auto text-center" style="max-width: 560px;">
        <h1 class="page-title text-danger">Note not found</h1>
        <p class="page-subtitle">Note ID: {escape(str(note_id))}</p>
        <a href="{escape(reverse('notes_list'))}" class="btn btn-primary">Return to notes</a>
    </div>
"""
        return HttpResponse(_html_shell("Not found", body), status=404)

    edit_url = reverse('note_edit', kwargs={'note_id': note["id"]})
    delete_url = reverse('note_delete', kwargs={'note_id': note["id"]})
    list_url = escape(reverse("notes_list"))

    body = f"""
    <div class="mx-auto" style="max-width: 760px;">
        <h1 class="page-title">{escape(note['title'])}</h1>

        <div class="mb-3 muted small">
            <span class="info-pill">ID: {note['id']}</span>
            <span class="info-pill">Tag: {escape(note['tag'])}</span>
            <span class="info-pill">Category: {escape(note['category'])}</span>
        </div>

        <div class="p-4 rounded-4 mb-4" style="background: #f7f9fd; border: 1px solid #e4ebf7;">
            {escape(note['body']).replace(chr(10), '<br />')}
        </div>

        <div class="actions-row">
            <a href="{edit_url}" class="btn btn-outline-primary">Edit</a>
            <a href="{delete_url}" class="btn btn-danger">Delete</a>
            <a href="{list_url}" class="btn btn-secondary ms-auto">Back to notes</a>
        </div>
    </div>
"""
    return HttpResponse(_html_shell(note["title"], body))

def _note_form_html(
    request: HttpRequest,
    *,
    action_url: str,
    title: str,
    heading: str,
    submit_label: str,
    cancel_url: str,
    title_val: str,
    body_val: str,
    tag_val: str,
    category_val: str,
    err: str,
) -> str:
    return f"""
    <div class="mx-auto" style="max-width: 700px;">
        <h1 class="page-title">{escape(heading)}</h1>
        <p class="page-subtitle">Fill in the fields below and submit.</p>

        {err}

        <form method="post" action="{escape(action_url)}">
            {_csrf_field(request)}

            <div class="mb-3">
                <label class="form-label">Title</label>
                <input type="text" name="title" class="form-control" value="{escape(title_val)}" required>
            </div>

            <div class="mb-3">
                <label class="form-label">Text</label>
                <textarea name="body" class="form-control" rows="6">{escape(body_val)}</textarea>
            </div>

            <div class="mb-3">
                <label class="form-label">Tag</label>
                <input type="text" name="tag" class="form-control" value="{escape(tag_val)}" placeholder="python">
            </div>

            <div class="mb-4">
                <label class="form-label">Category</label>
                <input type="text" name="category" class="form-control" value="{escape(category_val)}" placeholder="backend">
            </div>

            <div class="actions-row">
                <a href="{escape(cancel_url)}" class="btn btn-outline-secondary">Cancel</a>
                <button type="submit" class="btn btn-primary">{escape(submit_label)}</button>
            </div>
        </form>
    </div>
"""


def note_create(request: HttpRequest) -> HttpResponse:
    title_val = ""
    body_val = ""
    tag_val = ""
    category_val = ""

    if request.method == "POST":
        title = request.POST.get("title", "")
        note_body = request.POST.get("body", "")
        tag = request.POST.get("tag", "")
        category = request.POST.get("category", "")

        title_val, body_val, tag_val, category_val = title, note_body, tag, category

        if not title.strip():
            err = "<p class='mb-3' style='color: #b00020;'>Title cannot be empty.</p>"
        else:
            data.create_note(title=title, body=note_body, tag=tag or "misc", category=category or "general")
            return redirect("notes_list")
    else:
        err = ""

    form = _note_form_html(
        request,
        action_url=reverse("note_create"),
        title="Create note",
        heading="Create note",
        submit_label="Save",
        cancel_url=reverse("notes_list"),
        title_val=title_val,
        body_val=body_val,
        tag_val=tag_val,
        category_val=category_val,
        err=err,
    )
    return HttpResponse(_html_shell("Create note", form))


def note_edit(request: HttpRequest, note_id: int) -> HttpResponse:
    note = data.get_note(note_id)
    if note is None:
        body = f"""
    <h1 class="page-title text-danger">Cannot edit note</h1>
    <p class="muted">Note id: {escape(str(note_id))} not found.</p>
    <p><a href="{escape(reverse('notes_list'))}">Return to notes list</a></p>
"""
        return HttpResponse(_html_shell("404 not found", body), status=404)

    err = ""
    title_val = note["title"]
    body_val = note["body"]
    tag_val = note["tag"]
    category_val = note["category"]

    if request.method == "POST":
        title = request.POST.get("title", "")
        note_body = request.POST.get("body", "")
        tag = request.POST.get("tag", "")
        category = request.POST.get("category", "")

        title_val, body_val, tag_val, category_val = title, note_body, tag, category

        if not title.strip():
            err = "<p class='mb-3' style='color: #b00020;'>Title cannot be empty.</p>"
        else:
            data.update_note(
                note_id,
                title=title,
                body=note_body,
                tag=tag or "misc",
                category=category or "general",
            )
            return redirect("note_detail", note_id=note_id)

    form = _note_form_html(
        request,
        action_url=reverse("note_edit", kwargs={"note_id": note_id}),
        title="Edit note",
        heading="Edit note",
        submit_label="Save changes",
        cancel_url=reverse("note_detail", kwargs={"note_id": note_id}),
        title_val=title_val,
        body_val=body_val,
        tag_val=tag_val,
        category_val=category_val,
        err=err,
    )
    return HttpResponse(_html_shell("Edit note", form))


def note_delete(request: HttpRequest, note_id: int) -> HttpResponse:
    note = data.get_note(note_id)
    if note is None:
        body = f"""
        <h1 class="page-title text-danger">Cannot delete note</h1>
        <p class="muted">Note id: {escape(str(note_id))} not found.</p>
        <p><a href="{escape(reverse('notes_list'))}">Return to notes list</a></p>
        """
        return HttpResponse(_html_shell("404 not found", body), status=404)

    if request.method == "POST":
        data.delete_note(note_id)
        return redirect("notes_list")

    body = f"""
    <div class="mx-auto" style="max-width: 700px;">
        <h1 class="page-title">Delete note</h1>
        <p class="page-subtitle">This action cannot be undone.</p>

        <div class="p-3 rounded-4 mb-4" style="background: #fff4f4; border: 1px solid #f5cccc;">
            <strong>{escape(note['title'])}</strong>
            <div class="small muted">ID: {escape(str(note['id']))}</div>
        </div>

        <form method="post" action="{escape(reverse('note_delete', kwargs={'note_id': note_id}))}">
            {_csrf_field(request)}
            <div class="actions-row">
                <button type="submit" class="btn btn-danger">Delete</button>
                <a href="{escape(reverse('note_detail', kwargs={'note_id': note_id}))}" class="btn btn-outline-secondary">Cancel</a>
            </div>
        </form>
    </div>
    """
    return HttpResponse(_html_shell("Delete note", body))
