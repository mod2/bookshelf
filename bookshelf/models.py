from django.db import models
from django.contrib.auth.models import User
from autoslug import AutoSlugField
import datetime

class Book(models.Model):
    STATUSES = (
        ('active', 'Active'),
        ('deleted', 'Deleted'),
    )

    title = models.CharField(max_length=400)
    slug = AutoSlugField(populate_from='title')
    author = models.CharField(max_length=400, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUSES, default='active')
    date_published = models.CharField(max_length=100, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    isbn = models.CharField(max_length=20, null=True, blank=True)
    owner = models.ForeignKey(User, default=1)

    tags = models.ManyToManyField('Tag', null=True, blank=True)

    def __str__(self):
        return self.title


class Reading(models.Model):
    STATUSES = (
        ('active', 'Active'),
        ('finished', 'Finished'),
        ('abandoned', 'Abandoned'),
        ('deleted', 'Deleted'),
    )

    book = models.ForeignKey(Book)
    owner = models.ForeignKey(User, default=1)
    status = models.CharField(max_length=10, choices=STATUSES, default='active')

    started_date = models.DateField()
    goal_date = models.DateField(null=True, blank=True)
    finished_date = models.DateField(null=True, blank=True)

    start_page = models.PositiveSmallIntegerField(default=1)
    end_page = models.PositiveSmallIntegerField(null=True, blank=True)

    order = models.PositiveSmallIntegerField(default=100)

    folder = models.ForeignKey('Folder', null=True, blank=True, related_name='readings')

    tags = models.ManyToManyField('Tag', null=True, blank=True)

    def __str__(self):
        return "Reading for {}".format(self.book.title)

    def latest_entry(self):
        return self.entries.first()

    def current_page(self):
        latest_entry = self.latest_entry()

        if latest_entry:
            page_num = latest_entry.page_number
        else:
            page_num = 0

        return page_num

    def percentage(self):
        return (self.current_page() / self.end_page) * 100.0

    def pages_left(self):
        return self.end_page - self.current_page()

    def days_elapsed(self):
        first_entry = self.entries.last()
        #today = datetime.datetime.now()

        # TODO: fix
        return 5

    class Meta:
        ordering = ['order', 'started_date']


class Entry(models.Model):
    reading = models.ForeignKey(Reading, related_name='entries')
    page_number = models.PositiveSmallIntegerField()
    date = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(null=True, blank=True)
    owner = models.ForeignKey(User, default=1)

    def __str__(self):
        return "{} on {}".format(self.page_number, self.date)

    class Meta:
        ordering = ['page_number', '-date']
        verbose_name_plural = "entries"


class Folder(models.Model):
    name = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='name')
    order = models.PositiveSmallIntegerField(default=100)
    color = models.CharField(max_length=10, null=True, blank=True)
    owner = models.ForeignKey(User, default=1)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['order']


class Tag(models.Model):
    name = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='name')
    color = models.CharField(max_length=10, null=True, blank=True)
    owner = models.ForeignKey(User, default=1)

    def __str__(self):
        return self.name
