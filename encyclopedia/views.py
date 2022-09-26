from dataclasses import replace
from http.client import HTTPResponse
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
import markdown2 as md
from . import util
from bs4 import BeautifulSoup
import os
import random


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()})


def wiki(request, entry):
    try:
        content = md.markdown(util.get_entry(entry))
        entry = entry.lower().capitalize()
    except TypeError:
        return render(request, "./encyclopedia/error.html", {"entry": f"Page not fount for this entry: {entry}", "content": f"Page not fount for this entry: {entry}"+"\n"+"ERROR 404"})
    return render(request, "./encyclopedia/title.html", {"entry": entry, "content": content})


def search(request):
    if request.method == "GET":
        query_dict = request.GET
        query = query_dict.get('q', '')
        if not query or query == "":
            return render(request, "encyclopedia/search.html", {
                "found_entries": "", "query": query
            })
        else:
            entries = util.list_entries()
            similar_entries = [ent for ent in entries if query in ent]

            if len(similar_entries) == 1 and similar_entries[0].lower() == query.lower():
                return redirect('wiki', similar_entries[0])

            return render(request, "encyclopedia/search.html", {
                "found_entries": similar_entries, "query": query
            })


def new_page(request):
    title = request.GET.get("q", "")
    content = request.GET.get("text", "")
    if not title and not content:
        return render(request, "encyclopedia/newpage.html")
    entries = util.list_entries()
    check_title = [ent for ent in entries if title.lower() == ent.lower()]
    if check_title:
        return render(request, "./encyclopedia/error.html")
    with open(f"./entries/{title}.md", "a") as f:
        f.write(f"{content}")
    return redirect('wiki', title)


def edit_page(request, entry):
    entries = util.list_entries()
    title = [ent for ent in entries if ent.lower() == entry.lower()][0]
    content = util.get_entry(title)
    replacements = request.GET.get("text")
    if replacements == content and replacements:
        print("FUCK PYU")
        return render(request, "encyclopedia/editpage.html", {"content": content})
    elif replacements != content and replacements:
        with open(f"./entries/{title}.md", "w") as f:
            f.write(replacements)
        return redirect('wiki', title)
    return render(request, "encyclopedia/editpage.html", {"content": content})


def random_page(request):
    entries = util.list_entries()
    random_entry = entries[random.randint(0, len(entries)-1)]
    print(random_entry)
    return redirect('wiki', random_entry)
