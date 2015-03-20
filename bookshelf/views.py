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
