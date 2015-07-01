from django.utils import timezone
from django.utils.timezone import utc, make_aware
from datetime import datetime

from bookshelf.models import Reading, Entry

def get_stats_for_range(request, beginning, end):
    # Convert to UTC
    tz = timezone.get_current_timezone()
    d_tz = tz.normalize(beginning)
    beginning_utc = d_tz.astimezone(utc)
    d_tz = tz.normalize(end)
    end_utc = d_tz.astimezone(utc)

    # Get entries for the range
    entries = Entry.objects.filter(owner=request.user, date__gte=beginning_utc, date__lte=end_utc)

    # Pages read is just a sum of the entry amounts
    pages = sum(e.num_pages for e in entries)

    # Get books started/finished/abandoned during this range
    finished = Reading.objects.filter(owner=request.user, finished_date__gte=beginning_utc, finished_date__lte=end_utc, status='finished')
    started = Reading.objects.filter(owner=request.user, started_date__gte=beginning_utc, started_date__lte=end_utc)
    abandoned = started.filter(status='abandoned')

    # Percentage
    if len(started) > 0:
        abandoned_percentage = (len(abandoned) / len(started) * 100.0)
    else:
        abandoned_percentage = 0

    return {
        'pages': pages,
        'finished': len(finished),
        'finished_titles': '; '.join([b.book.title for b in finished.order_by('finished_date')]),
        'started': len(started),
        'started_titles': '; '.join([b.book.title for b in started.order_by('started_date')]),
        'abandoned': len(abandoned),
        'abandoned_titles': '; '.join([b.book.title for b in abandoned.order_by('started_date')]),
        'abandoned_percentage': abandoned_percentage,
    }
