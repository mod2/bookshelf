from django.utils import timezone
from django.utils.timezone import utc, make_aware
from datetime import datetime, timedelta

from bookshelf.models import Reading, Entry, Tag

def get_stats_for_range(request, beginning, end, get_titles=False):
    # Convert to UTC
    tz = timezone.get_current_timezone()
    d_tz = tz.normalize(beginning)
    beginning_utc = d_tz.astimezone(utc)
    d_tz = tz.normalize(end)
    end_utc = d_tz.astimezone(utc)

    # Get entries for the range
    entries = Entry.objects.filter(owner=request.user, date__gte=beginning_utc, date__lte=end_utc).values('num_pages')

    # Pages read is just a sum of the entry amounts
    pages = sum(e['num_pages'] for e in entries)

    # Get books started/finished/abandoned during this range
    finished = Reading.objects.filter(owner=request.user, finished_date__gte=beginning_utc, finished_date__lte=end_utc, status='finished')
    started = Reading.objects.filter(owner=request.user, started_date__gte=beginning_utc, started_date__lte=end_utc)
    abandoned = started.filter(status='abandoned')

    # Percentage
    if len(started) > 0:
        abandoned_percentage = (len(abandoned) / len(started) * 100.0)
    else:
        abandoned_percentage = 0

    response = {
        'pages': pages,
        'finished': len(finished),
        'started': len(started),
        'abandoned': len(abandoned),
        'abandoned_percentage': abandoned_percentage,
    }

    if get_titles:
        response['finished_titles'] = '; '.join([b.book.title for b in finished.order_by('finished_date')])
        response['started_titles'] = '; '.join([b.book.title for b in started.order_by('started_date')])
        response['abandoned_titles'] = '; '.join([b.book.title for b in abandoned.order_by('started_date')])

    return response

def get_stats_for_week(request):
    # Last 7 days
    end = timezone.now()
    beginning = end - timedelta(7)

    # Convert to UTC
    tz = timezone.get_current_timezone()
    d_tz = tz.normalize(beginning)
    beginning_utc = d_tz.astimezone(utc)
    d_tz = tz.normalize(end)
    end_utc = d_tz.astimezone(utc)

    # Get entries for the range
    entries = Entry.objects.filter(
        owner=request.user,
        date__gte=beginning_utc,
        date__lte=end_utc,
    ).prefetch_related('reading').values('num_pages', 'reading__tags')

    tags = {}
    total = 0

    # Sum up the pages read for each tag
    for e in entries:
        t = e['reading__tags']
        if t not in tags:
            tags[t] = 0
        tags[t] += e['num_pages']
        total += e['num_pages']

    # Now put it all together
    response = []
    for t in tags:
        tag = Tag.objects.get(id=t)
        response.append({
            'label': tag.slug,
            'percentage': (tags[t] / total * 100),
        })

    # Sort it
    response = sorted(response, key=lambda k: k['label'])

    return response
