# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render_to_response
from django.db.models import Q

from .models import Book, Reading, Entry, Folder

from datetime import datetime
import json

@login_required
def dashboard(request):
    folders = Folder.objects.filter(owner=request.user)
    folder = {
        'slug': 'dashboard',
    }


    folderless = Reading.objects.filter(owner=request.user, folder=None)

    return render_to_response('dashboard.html', {'folders': folders,
                                              'folder': folder,
                                              'folderless': folderless,
                                              'request': request })

@login_required
def book(request, book_slug):
    book = Book.objects.get(slug=book_slug, owner=request.user)
    folders = Folder.objects.filter(owner=request.user)

    folderless = Reading.objects.filter(owner=request.user, folder=None)

    return render_to_response('book.html', {'book': book,
                                            'title': book.title,
                                            'folders': folders,
                                            'folderless': folderless,
                                            'request': request })


@login_required
def folder(request, folder_slug):
    folder = Folder.objects.get(slug=folder_slug, owner=request.user)
    folders = Folder.objects.filter(owner=request.user)

    folderless = Reading.objects.filter(owner=request.user, folder=None)

    return render_to_response('folder.html', {'folder': folder,
                                              'title': folder.name,
                                              'folders': folders,
                                              'folderless': folderless,
                                              'request': request })

@login_required
def add_book(request):
    if request.method == 'GET':
        folders = Folder.objects.filter(owner=request.user)
        folderless = Reading.objects.filter(owner=request.user, folder=None)

        return render_to_response('add.html', {'folders': folders,
                                               'title': 'Add Book',
                                               'folderless': folderless,
                                               'request': request })
    elif request.method == 'POST':
        try:
            title = request.POST.get('title', '')
            author = request.POST.get('author', '')
            num_pages = int(request.POST.get('num_pages', 0))
            starting_page = int(request.POST.get('starting_page', 1))

            if title != '':
                # Create the book
                book = Book()
                book.title = title
                book.owner = request.user
                if author:
                    book.author = author
                book.save()

                # Create the reading
                reading = Reading()
                reading.owner = request.user
                reading.book = book
                reading.started_date = datetime.now()
                reading.start_page = starting_page
                reading.end_page = num_pages
                reading.save()

                # Return the book and reading IDs
                response = { 'status': 200, 'reading_id': reading.id, 'book_id': book.id }
            else:
                response = { 'status': 500, 'message': "Missing title" }
        except Exception as e:
            response = { 'status': 500, 'message': "Couldn't add book" }

        return JsonResponse(response)


@login_required
def edit_book(request, book_slug):
    book = Book.objects.get(slug=book_slug)
    folders = Folder.objects.filter(owner=request.user)
    folderless = Reading.objects.filter(owner=request.user, folder=None)

    return render_to_response('book.html', {'book': book,
                                            'title': '{} — Edit'.format(book.title),
                                            'folders': folders,
                                            'folderless': folderless,
                                            'request': request })

@login_required
def search(request):
    query = request.GET.get('q', '')

    folders = Folder.objects.filter(owner=request.user)
    folderless = Reading.objects.filter(owner=request.user, folder=None)

    if query != '':
        results = Reading.objects.filter(
            Q(book__title__contains=query)
            | Q(book__author__contains=query)
        )

    return render_to_response('results.html', {'folders': folders,
                                               'title': '{} — Search'.format(query),
                                               'folderless': folderless,
                                               'results': results,
                                               'query': query,
                                               'request': request })


def api_folder_update_order(request):
    order = request.GET.get('order', '')
    slug_list = order.split(',')

    try:
        for s, folder_slug in enumerate(slug_list):
            folder_slug = slug_list[s]
            folder = Folder.objects.get(slug=folder_slug)
            folder.order = s
            folder.save()
        response = { 'status': 200 }
    except:
        response = { 'status': 500, 'message': "Couldn't update orders" }

    return JsonResponse(response)

def api_reading_update_order(request):
    order = request.GET.get('order', '')
    id_list = order.split(',')

    try:
        for i, reading_id in enumerate(id_list):
            reading_id = id_list[i]
            reading = Reading.objects.get(id=reading_id)
            reading.order = i
            reading.save()
        response = { 'status': 200 }
    except:
        response = { 'status': 500, 'message': "Couldn't update orders" }

    return JsonResponse(response)

def api_reading_add_entry(request):
    """ Add a new entry for a reading """

    if request.method == 'POST':
        try:
            reading_id = int(request.POST.get('reading_id', -1))
            page_number = int(request.POST.get('page_number', -1))
            comment = request.POST.get('comment', '')

            reading = Reading.objects.get(id=reading_id)

            entry = Entry()
            entry.reading = reading

            if page_number == -1:
                # If they didn't put a page number, use either the latest
                # page number or just put 1
                latest_entry = reading.latest_entry()
                if latest_entry:
                    entry.page_number = latest_entry.page_number
                else:
                    entry.page_number = 1
            else:
                entry.page_number = page_number

            if comment != '':
                entry.comment = comment

            entry.save()

            response = {'status': 200,
                        'reading_id': reading.id,
                        'page_number': entry.page_number,
                        'pages_left': reading.pages_left(),
                        'percentage': reading.percentage(),
                       }
        except Exception as e:
            print(e)
            response = { 'status': 500, 'message': "Couldn't add entry" }
    else:
        response = { 'status': 500, 'message': "Couldn't add entry" }

    return JsonResponse(response)

def api_search(request):
    query = request.GET.get('q', '')

    if query != '':
        try:
            results = Reading.objects.filter(
                Q(book__title__contains=query)
                | Q(book__author__contains=query)
            )

            data = [r.to_dict() for r in results]

            response = { 'status': 200, 'results': data }
        except Exception as e:
            response = { 'status': 500, 'message': "Bad query" }
    else:
        response = { 'status': 500, 'message': "Empty query" }

    return JsonResponse(response)
