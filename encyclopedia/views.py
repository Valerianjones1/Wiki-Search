from django.shortcuts import render, redirect

import markdown2 as md
from . import util
from bs4 import BeautifulSoup


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def title(request, entry):
    return render(request, "./encyclopedia/title.html", {"entry": entry.lower().capitalize(), "content": md.markdown(util.get_entry(entry))})


def search(request, query):

    entries = util.list_entries()
    for ent in entries:
        if query.lower() == entries.lower():
            return redirect(f"/{ent}")
        elif query in ent:
            return render(request, "./encyclopedia/search.html", {"query": query, "entry": ent, "entries": util.list_entries()})
    return render(request, "./encyclopedia/search.html", {"query": query, "entries": util.list_entries()})
