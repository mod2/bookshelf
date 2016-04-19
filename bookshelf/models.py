# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from autoslug import AutoSlugField
from django.utils import timezone
from django.utils.timezone import utc
import datetime
from datetime import timedelta
import math

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

    tags = models.ManyToManyField('Tag', blank=True)

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

    stale_period = models.PositiveSmallIntegerField(default=0)

    tags = models.ManyToManyField('Tag', blank=True)

    def __str__(self):
        return "Reading for {}".format(self.book.title)

    def latest_entry(self):
        return self.entries.first()

    def total_pages(self):
        if self.end_page:
            return self.end_page - (self.start_page - 1)
        else:
            return 0

    def current_page(self):
        latest_entry = self.latest_entry()

        if latest_entry:
            page_num = latest_entry.page_number
        else:
            page_num = 0

        return page_num

    def percentage(self):
        if self.end_page:
            if self.current_page() < self.start_page:
                return 0

            return int(((self.current_page() - (self.start_page - 1)) / self.total_pages()) * 100.0)
        else:
            return 0

    def pages_left(self):
        if self.end_page:
            if self.current_page() < self.start_page:
                return self.total_pages()

            return self.end_page - self.current_page()
        else:
            return 0

    def pages_per_day_for_goal(self):
        days = self.days_left_to_goal()
        pages = self.pages_left()
        if days > 0:
            return round(pages / days, 1)
        else:
            return pages

    def read_to_page_for_goal(self):
        current_page = self.current_page()
        return math.ceil(current_page + self.pages_per_day_for_goal())

    def days_elapsed(self):
        first_entry = self.entries.last().date.replace(tzinfo=utc).replace(hour=0, minute=0, second=0, microsecond=0)
        today = datetime.datetime.now().replace(tzinfo=utc).replace(hour=0, minute=0, second=0, microsecond=0)

        return (today - first_entry).days

    def days_since_last_entry(self):
        if self.entries.count() > 0:
            last_entry = self.entries.first().date.replace(tzinfo=utc).astimezone(tz=None).replace(hour=0, minute=0, second=0, microsecond=0)
            today = datetime.datetime.utcnow().replace(tzinfo=utc).astimezone(tz=None).replace(hour=0, minute=0, second=0, microsecond=0)

            return (today - last_entry).days
        else:
            return 0

    def days_since_last_entry_label(self):
        days = self.days_since_last_entry()
        
        if days == 0:
            return "today"
        elif days == 1:
            return "1 day ago"
        else:
            return "{} days ago".format(days)

    def days_left_to_goal(self):
        today = datetime.date.today()
        return (self.goal_date - today).days

    def get_stale_period(self):
        from django.conf import settings

        # If the reading has a stale period, use it instead of the system default
        if self.stale_period > 0:
            stale_period = self.stale_period
        else:
            stale_period = settings.STALE_PERIOD

        return stale_period

    def stale(self):
        stale_period = self.get_stale_period()

        if not self.finished_date and stale_period != 0 and self.days_since_last_entry() > stale_period:
            return True

        return False

    def to_dict(self):
        try:
            response = {
                'book': {
                    'id': self.book.id,
                    'title': self.book.title,
                    'author': self.book.author,
                },
                'owner': self.owner.id,
                'status': self.status,
                'started_date': self.started_date,
                'goal_date': self.goal_date,
                'finished_date': self.finished_date,
                'start_page': self.start_page,
                'end_page': self.end_page,
                'total_pages': self.total_pages(),
                'tags': [t.name for t in self.tags.all()]
            }
        except Exception as e:
            print(e)

        return response

    def taglist(self):
        """ Returns a list of the tag slugs applied to this reading. """

        return [t.slug for t in self.tags.all()]

    class Meta:
        ordering = ['order', 'started_date']


class Entry(models.Model):
    reading = models.ForeignKey(Reading, related_name='entries')
    page_number = models.PositiveSmallIntegerField()
    num_pages = models.PositiveSmallIntegerField(null=True, blank=True)
    date = models.DateTimeField()
    comment = models.TextField(null=True, blank=True)
    owner = models.ForeignKey(User, default=1)

    def __str__(self):
        return "{} on {}".format(self.page_number, self.date)

    def save(self, *args, **kwargs):
        if not self.date:
            self.date = datetime.datetime.now()

        if not self.num_pages:
            if self.reading.entries.count() > 0:
                self.num_pages = self.page_number - self.reading.entries.first().page_number
            else:
                self.num_pages = self.page_number

        return super(Entry, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-date', '-page_number']
        verbose_name_plural = "entries"


class Tag(models.Model):
    name = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='name')
    color = models.CharField(max_length=10, null=True, blank=True)
    owner = models.ForeignKey(User, default=1)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['slug']
