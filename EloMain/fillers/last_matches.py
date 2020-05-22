from concurrent.futures import ProcessPoolExecutor
from datetime import datetime

from django.http import HttpResponse

from EloMain.models import Championship
from EloMain.tasks import fill_championship, Stats


def fill_last_matches(request):
    champs = Championship.objects.all()

    date_str = "14.5.20"
    filter_date = datetime.strptime(date_str, "%d.%m.%y")
    date_str2 = "22.3.21"
    filter_date2 = datetime.strptime(date_str2, "%d.%m.%y")
    stats = Stats()
    stats.await_matches = 0
    stats.counter = 0
    stats.filter_date = filter_date
    stats.filter_date2 = filter_date2

    pool = ProcessPoolExecutor(16)
    futures = []
    for champ in champs:
        fill_championship.delay(champ.id, stats.filter_date, stats.filter_date2)

    return HttpResponse('done')

