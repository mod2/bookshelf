from django.contrib import admin
from .models import Book, Reading, Entry, Tag


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'isbn', 'date_published', 'date_added', 'status', 'owner')
    pass


@admin.register(Reading)
class ReadingAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'started_date', 'finished_date', 'start_page', 'end_page', 'owner')
    pass


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ('reading', 'page_number', 'num_pages', 'date', 'comment', 'owner')
    pass


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'color', 'owner')
    pass
