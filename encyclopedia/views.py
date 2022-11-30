from django.shortcuts import render
from . import util
from markdown2 import Markdown
from re import match
from random import choice


def index(request):
    return render(request, "encyclopedia/index.html", {"entries": util.list_entries()})

def page_entry(request, title):
    wiki_pages = util.list_entries()
    if title in wiki_pages:
        markdowner = Markdown()
        converted_md = markdowner.convert(util.get_entry(title))
        return render(request, "encyclopedia/page.html", {"title":title, "converted": converted_md})
    else:
        return render(request, "encyclopedia/page.html", 
        {"title":"PAGE NOT FOUND", "error": f"ERROR {title.upper()} PAGE DOES NOT EXIST"})

def results(request):
        wiki_pages = util.list_entries()
        if request.method == "POST":
            search_word = request.POST["search_term"]
            if search_word in wiki_pages:
                return page_entry(request, search_word)
            #use regex
            else:
                search_options = []
                for each_title in wiki_pages:
                    partial_match = match(f'.*{search_word}.*', each_title)   
                    if partial_match:
                        search_options.append(partial_match.group(0))
                return render(request, "encyclopedia/results.html",{"results": search_word, "result_here":search_options})

def new_page(request):
    if request.method == "POST":
        wiki_pages = util.list_entries()
        title = request.POST["title"]
        content = request.POST["content"]
        if title in wiki_pages:
            return render(request, "encyclopedia/new_page.html", {"already_exists": title})
        else:
            util.save_entry(title, content)
            return page_entry(request, title)
    else:
        return render(request, "encyclopedia/new_page.html")

def edit(request, title):
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        util.save_entry(title,content)
        return page_entry(request,title)
    else:
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html",{"page_title": title,"content":content})

def random(request):
    wiki_pages = util.list_entries()
    title = choice(wiki_pages)
    markdowner = Markdown()
    converted_md = markdowner.convert(util.get_entry(title))
    return render(request, "encyclopedia/page.html", {"title":title, "converted": converted_md})