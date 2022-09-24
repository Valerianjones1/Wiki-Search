from django.shortcuts import render, redirect

import markdown2 as md
from . import util
from bs4 import BeautifulSoup


def index(request):
    if request.method == "GET":
        query_dict = request.GET
        query = query_dict.get('q')
        print(query, "IAMHERE")
        if not query:
            return render(request, "encyclopedia/index.html", {
                "entries": util.list_entries()
            })
        else:
            entries = util.list_entries()
            for ent in entries:
                if query.lower() == ent.lower():
                    return redirect(f"http://127.0.0.1:8000/{ent}")
                elif query in ent:
                    return render(request, "./encyclopedia/search.html", {"query": query, "entry": ent, "entries": entries})


def title(request, entry):
    content = md.markdown(util.get_entry(entry))
    entry = entry.lower().capitalize()
    return render(request, "./encyclopedia/title.html", {"entry": entry, "content": content})


def search(request):
    query_dict = request.GET
    query = query_dict.get('q')
    print(query, query_dict, "IAMHERE")
    if not query:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
        })
    else:
        entries = util.list_entries()
        for ent in entries:
            if query.lower() == ent.lower():
                return redirect(f"http://127.0.0.1:8000/{ent}")
            elif query in ent:
                return render(request, "./encyclopedia/index.html", {"query": query, "entry": ent, "entries": entries})
