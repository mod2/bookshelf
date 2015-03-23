# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render_to_response

from .models import Book, Reading, Folder

@login_required
def dashboard(request):
    folders = Folder.objects.filter(owner=request.user)
    folder = folders.first()

    folderless = Reading.objects.filter(owner=request.user, folder=None)

    return render_to_response('folder.html', {'folders': folders,
                                              'folder': folder,
                                              'folderless': folderless,
                                              'request': request })

@login_required
def current(request):
    folders = Folder.objects.filter(owner=request.user)
    folder = {
        'slug': 'current',
    }

    folderless = Reading.objects.filter(owner=request.user, folder=None)

    return render_to_response('current.html', {'folders': folders,
                                           'folder': folder,
                                           'folderless': folderless,
                                           'request': request })

@login_required
def book(request, book_slug):
    book = Book.objects.get(slug=book_slug, owner=request.user)
    folders = Folder.objects.filter(owner=request.user)

    folderless = Reading.objects.filter(owner=request.user, folder=None)

    return render_to_response('book.html', {'book': book,
                                            'folders': folders,
                                            'folderless': folderless,
                                            'request': request })


@login_required
def folder(request, folder_slug):
    folder = Folder.objects.get(slug=folder_slug, owner=request.user)
    folders = Folder.objects.filter(owner=request.user)

    folderless = Reading.objects.filter(owner=request.user, folder=None)

    return render_to_response('folder.html', {'folder': folder,
                                              'folders': folders,
                                              'folderless': folderless,
                                              'request': request })

@login_required
def add_book(request):
    folders = Folder.objects.filter(owner=request.user)
    folderless = Reading.objects.filter(owner=request.user, folder=None)

    return render_to_response('book.html', {'folders': folders,
                                            'folderless': folderless,
                                            'request': request })

@login_required
def edit_book(request, book_slug):
    book = Book.objects.get(slug=book_slug)
    folders = Folder.objects.filter(owner=request.user)
    folderless = Reading.objects.filter(owner=request.user, folder=None)

    return render_to_response('book.html', {'book': book,
                                            'folders': folders,
                                            'folderless': folderless,
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
