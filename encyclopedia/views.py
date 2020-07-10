import random as rmd
from django.shortcuts import render
from django.http import HttpResponseRedirect
from markdown2 import Markdown
from django.urls import reverse
from django import forms

from . import util

#Setting Markdown Variable
mark = Markdown()

#class to work with django forms POST Method | GET Method for search bar
class SearchForm(forms.Form):
    data = forms.CharField()

#Class for input the information from new create page
class NewPage(forms.Form):
    title = forms.CharField()
    info = forms.CharField(widget=forms.Textarea(), label='')

#Class for the edit page to display the text Areas
class EditPage(forms.Form):
    info = forms.CharField(widget=forms.Textarea(), label='')


#Index Page to load front Page
def index(request):
    return render(request, "encyclopedia/index.html", {"entries": util.list_entries(),"form":SearchForm()})

#Entery Page for a perticular requested entry
def entry(request,name):
    pages = util.list_entries()
    #If entered string is valid
    if name in pages:
        page = util.get_entry(name)
        page = mark.convert(page)
        return render(request,"encyclopedia/entry.html",{"page":page,"name":name,"form":SearchForm()})
    #if entered string is not valid
    else:
        return render(request,"encyclopedia/error.html",{"message": "Sorry page Not found!","form":SearchForm()})

#user Request to search for perticular strnig or substring
def search(request):
    entries = util.list_entries()
    array = []
    form = SearchForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data["data"]
        #loop through the number of entries in list of enteries
        for i in entries:
            if data is i:
                array.append(i)
            elif data.lower() in i.lower():
                array.append(i)

        #returning collected Data (main strings matching and substrings)
        return render(request,"encyclopedia/search.html",{"pages":array,"title":data,"form":SearchForm()})
    # If the from is not valid
    return render(request, "encyclopedia/index.html", {"form":form})


#User Request to create a new page on a Wiki Site. And Page Name must not Exist twice
def create(request):
    #if Method is GET
    if request.method == 'GET':
        return render(request,"encyclopedia/create.html",{"form":SearchForm(),"page":NewPage()})

    #IF THIS NOT A CASE THEN
    entries = util.list_entries()
    form = NewPage(request.POST)
    if form.is_valid():
        title = form.cleaned_data["title"]
        info = form.cleaned_data["info"]
        #if the new page title is already existed in the entires
        if title in entries:
            return render(request,"encyclopedia/error.html" ,{"message": "Page Already Exist.Please try something else."})

        #Given title is for a unique page
        util.save_entry(title,info)
        recentPage = util.get_entry(title)
        recentPage = mark.convert(recentPage)
        return render(request,"encyclopedia/entry.html",{"name":title,"page":recentPage,"form":SearchForm()})

#When User requested to Edit a perticular Page
def edit(request,name):
    if request.method == 'GET':
        page = util.get_entry(name)
        return render(request,"encyclopedia/edit.html",{"form":SearchForm(),"editArea":EditPage(initial={'info': page}),"name":name})

    #If this is a POST request
    form = EditPage(request.POST)
    if form.is_valid():
        info = form.cleaned_data["info"]
        util.save_entry(name,info)
        page = util.get_entry(name)
        page = mark.convert(page)
        return render(request,"encyclopedia/entry.html",{"form":SearchForm(),"page": page,"name": name})

# This function will execute when user click on a random button on the Site
def random(request):
    entries = util.list_entries()
    title = rmd.choice(entries)
    page = util.get_entry(title)
    page = mark.convert(page)
    return render(request,"encyclopedia/entry.html",{"form":SearchForm(),"page":page,"name": title})
