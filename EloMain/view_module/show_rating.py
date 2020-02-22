import time
from datetime import date
import calendar

from django.db.models import Q
from django.shortcuts import render
from EloMain.models import Change, Championship, Club


def month_rating(request):
    date1 = date.today()
    changes = (
        Change.objects.all()
        .filter(rating_after__gte=1000)
        .filter(
            game__date__gte=date(date1.year, date1.month, 1),
            game__date__lt=date(date1.year, date1.month, calendar.monthrange(date1.year, date1.month)[1]),
        )
    )
    clubs = {}
    for change in changes:
        if not change.club in clubs:
            clubs[change.club] = change.rating_delta
        else:
            clubs[change.club] += change.rating_delta
    clubs = [(k, clubs[k]) for k in sorted(clubs, key=clubs.get, reverse=True)]

    return render(request, "EloMain/month_rating.html", locals())


def year_rating(request):
    start_time = time.time()
    year = date.today().year
    changes = Change.objects.filter(game__date__gte=date(year, 1, 1), game__date__lte=date(year, 12, 31))
    print("Time elapsed: {}".format(time.time() - start_time))
    start_time = time.time()
    clubs = {}
    for change in changes.iterator():
        if not change.club in clubs:
            clubs[change.club] = change.rating_delta
        else:
            clubs[change.club] += change.rating_delta
    print("Time elapsed: {}".format(time.time() - start_time))
    start_time = time.time()
    clubs = [(k, clubs[k]) for k in sorted(clubs, key=clubs.get, reverse=True)]
    print("Time elapsed: {}".format(time.time() - start_time))

    return render(request, "EloMain/year_rating.html", locals())


def show_country_rating(request):
    tourns = Championship.objects.filter(elo_index=30)
    champs = []
    for champ in tourns:
        clubs = Club.objects.filter(championship=champ).order_by("-rating").filter(~Q(name="Москва"))
        clubs = clubs[:10]
        total = 0
        for club in clubs:
            total += club.rating
        champs.append((champ, round(total / 10, 2), "rating/{}".format(champ.id)))
    champs.sort(key=lambda x: -x[1])

    print(champs)

    return render(request, "EloMain/country_rating.html", locals())


def top_delta(request):
    changes = Change.objects.order_by("-rating_delta")
    changes = changes[:5]
    return render(request, "EloMain/top_changes.html", locals())


def top_rating_ever(request):
    start_time = time.time()
    changes = Change.objects.all().order_by("-rating_after")
    used_clubs = []
    top = []
    i = 0
    while len(top) < 5:
        change = changes[i]
        if change.club not in used_clubs:
            top.append(change)
            used_clubs.append(change.club)
        i += 1
    print("Time elapsed: {}".format(time.time() - start_time))

    return render(request, "EloMain/top_rating_ever.html", locals())
