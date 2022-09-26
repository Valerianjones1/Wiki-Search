from http.client import HTTPResponse
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
import markdown2 as md
from . import util
from bs4 import BeautifulSoup


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()})


def wiki(request, entry):
    try:
        content = md.markdown(util.get_entry(entry))
        entry = entry.lower().capitalize()
    except TypeError:
        return render(request, "./encyclopedia/title.html", {"entry": f"Page not fount for this entry: {entry}", "content": f"Page not fount for this entry: {entry}"+"\n"+"ERROR 404"})
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
            # if not similar_entries:
            #     return render(request, "encyclopedia/search.html", {
            #     "found_entries": similar_entries, "query": query
            # })
            if len(similar_entries) == 1 and similar_entries[0].lower() == query.lower():
                return redirect('wiki', similar_entries[0])

            return render(request, "encyclopedia/search.html", {
                "found_entries": similar_entries, "query": query
            })
