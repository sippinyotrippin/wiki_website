from markdown2 import Markdown
from django.shortcuts import render

from . import util
from random import choice


def convert_md_to_html(title):
    content = util.get_entry(title)
    markdowner = Markdown()
    if content is None:
        return None
    else:
        return markdowner.convert(content)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    html_content = convert_md_to_html(title)
    if html_content is None:
        return render(request, "encyclopedia/error.html", {
            "title_name": title
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title_name": title,
            "md_content": html_content
        })


def search(request):
    if request.method == "POST":
        entry_search = request.POST['q']
        html_content = convert_md_to_html(entry_search)
        results = []
        if html_content is not None:
            return render(request, "encyclopedia/entry.html", {
                "title_name": entry_search,
                "md_content": html_content
            })
        else:
            for page in util.list_entries():
                if entry_search.lower() == page.lower():
                    return render(request, "encyclopedia/entry.html", {
                        "title_name": page,
                        "md_content": convert_md_to_html(page)
                    })
                elif entry_search.lower() in page.lower():
                    results.append(page)
            if results:
                return render(request, "encyclopedia/didyoumean.html", {
                    "your_search": entry_search,
                    "results": results
                })
            else:
                return render(request, "encyclopedia/search_error.html", {
                    "page": entry_search
                })


def new_page(request):
    if request.method == "GET":
        return render(request, "encyclopedia/create_new_page.html")
    else:
        title = request.POST['title']
        content = request.POST['content']
        if title in util.list_entries():
            return render(request, "encyclopedia/create_error.html")
        else:
            util.save_entry(title, content)
            html_content = convert_md_to_html(title)
            return render(request, "encyclopedia/entry.html", {
                "title_name": title,
                "md_content": html_content
            })


def edit_page(request):
    if request.method == "POST":
        title = request.POST.get('title_')
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "md_content": content
        })


def save_edit(request):
    if request.method == "POST":
        prev = request.POST.get('previous_title')
        title = request.POST.get('edit_title')
        content = request.POST.get('edit_content')
        util.save_entry(title, content)
        if title != prev:
            util.default_storage.delete(f"entries/{prev}.md")
        return render(request, "encyclopedia/entry.html", {
            "title_name": title,
            "md_content": convert_md_to_html(title)
        })


def random_page(request):
    entries = util.list_entries()
    random_entry = choice(entries)
    return render(request, "encyclopedia/entry.html", {
        "title_name": random_entry,
        "md_content":  convert_md_to_html(random_entry)
    })
