from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    url(r'^login/', 'django.contrib.auth.views.login', { 'template_name': 'login.html' }, name='login'),
    url(r'^logout/', 'django.contrib.auth.views.logout', { 'template_name': 'logout.html', 'next_page': '/login/' }, name='logout'),

    url(r'^book/(.+?)/$', 'bookshelf.views.book', name='book'),
    url(r'^folder/(.+?)/$', 'bookshelf.views.folder', name='folder'),
    url(r'^current/$', 'bookshelf.views.current', name='current'),
    url(r'^$', 'bookshelf.views.dashboard', name='dashboard'),

    # Web services
    #url(r'^api/book/(.+?)/reorder-scenes/$', 'storybook.views.ws_reorder_scenes', name='ws_reorder_scenes'),
)
