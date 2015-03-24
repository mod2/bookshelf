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
        if self.end_page:
            return int((self.current_page() / self.end_page) * 100.0)
        else:
            return 0

    def pages_left(self):
        if self.end_page:
            return self.end_page - self.current_page()
        else:
            return 0

    def days_elapsed(self):
        first_entry = self.entries.last()
        #today = datetime.datetime.now()

        # TODO: fix
        return 5

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
                'folder': {
                    'id': self.folder.id if self.folder else None,
                    'name': self.folder.name if self.folder else None,
                },
                'tags': [t.name for t in self.tags.all()]
            }
        except Exception as e:
            print(e)

        return response

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
            if len(self.reading.entries.all()) > 0:
                self.num_pages = self.page_number - self.reading.entries.first().page_number
            else:
                self.num_pages = self.page_number

        return super(Entry, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-date', '-page_number']
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
