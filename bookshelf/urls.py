from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from django.contrib import admin

from bookshelf import views as bookshelf_views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    url(r'^login/', auth_views.login, { 'template_name': 'login.html' }, name='login'),
    url(r'^logout/', auth_views.logout, { 'template_name': 'logout.html', 'next_page': '/login/' }, name='logout'),

    url(r'^book/(.+?)/edit/$', bookshelf_views.edit_book, name='edit_book'),
    url(r'^book/(.+?)/abandon/$', bookshelf_views.abandon_book, name='abandon_book'),
    url(r'^book/(.+?)/(.+?)/$', bookshelf_views.book, name='book'),
    url(r'^$', bookshelf_views.dashboard, name='dashboard'),

    url(r'^add/$', bookshelf_views.add_book, name='add_book'),
    url(r'^search/$', bookshelf_views.search, name='search'),
    url(r'^history/$', bookshelf_views.history, name='history'),
    url(r'^stats/$', bookshelf_views.stats, name='stats'),

    # Web services
    url(r'^api/reading/update-order/$', bookshelf_views.api_reading_update_order, name='api_reading_update_order'),
    url(r'^api/reading/add-entry/$', bookshelf_views.api_reading_add_entry, name='api_reading_add_entry'),
    url(r'^api/search/$', bookshelf_views.api_search, name='api_search'),
]
