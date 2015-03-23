from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    url(r'^login/', 'django.contrib.auth.views.login', { 'template_name': 'login.html' }, name='login'),
    url(r'^logout/', 'django.contrib.auth.views.logout', { 'template_name': 'logout.html', 'next_page': '/login/' }, name='logout'),

    url(r'^book/(.+?)/edit/$', 'bookshelf.views.edit_book', name='edit_book'),
    url(r'^book/(.+?)/$', 'bookshelf.views.book', name='book'),
    url(r'^folder/(.+?)/$', 'bookshelf.views.folder', name='folder'),
    url(r'^$', 'bookshelf.views.dashboard', name='dashboard'),

    url(r'^add/$', 'bookshelf.views.add_book', name='add_book'),

    # Web services
    url(r'^api/folder/update-order/$', 'bookshelf.views.api_folder_update_order', name='api_folder_update_order'),
    url(r'^api/reading/update-order/$', 'bookshelf.views.api_reading_update_order', name='api_reading_update_order'),
)
