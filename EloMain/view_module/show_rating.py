from datetime import date, time
from django.shortcuts import render
from EloMain.models import Change


def month_rating(request):
    date1 = date.today()
    changes = Change.objects.all().filter(rating_after__gte=1100).filter(game__date__gte=date(date1.year,date1.month,1),
                                       game__date__lt=date(date1.year,date1.month,31))
    clubs = {}
    for change in changes:
        if not change.club in clubs:
            clubs[change.club] = change.rating_delta
        else:
            clubs[change.club] += change.rating_delta
    clubs = [(k,clubs[k]) for k in sorted(clubs, key=clubs.get, reverse=True)]

    return render(request, 'EloMain/month_rating.html', locals())

def year_rating(request):
    start_time = time.time()
    year = 2019
    changes = Change.objects.all().filter(game__date__gte=date(year,1,1),
                                       game__date__lte=date(year,12,31))
    print("Time elapsed: {}".format(time.time() - start_time))
    start_time = time.time()
    clubs = {}
    for change in changes:
        if not change.club in clubs:
            clubs[change.club] = change.rating_delta
        else:
            clubs[change.club] += change.rating_delta
    print("Time elapsed: {}".format(time.time() - start_time))
    start_time = time.time()
    clubs = [(k,clubs[k]) for k in sorted(clubs, key=clubs.get, reverse=True)]
    print("Time elapsed: {}".format(time.time()-start_time))

    return render(request, 'EloMain/year_rating.html', locals())