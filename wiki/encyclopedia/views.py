from markdown2 import Markdown
from django.shortcuts import render

from . import util


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
        your_search = entry_search
        html_content = convert_md_to_html(entry_search)
        if html_content is None:
            for entry_item in util.list_entries():
                if entry_search in entry_item:
                    entry_search = entry_item
                    return render(request, 'encyclopedia/didyoumean.html', {
                        "page_name": entry_search,
                        "your_search": your_search
                    })
            return render(request, "encyclopedia/found_pages.html", {
                "page": entry_search
            })

        else:
            return render(request, "encyclopedia/entry.html", {
                "title_name": entry_search,
                "md_content": html_content
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
    pass