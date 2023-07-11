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