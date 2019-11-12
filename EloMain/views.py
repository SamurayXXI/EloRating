from datetime import datetime
from django.db.models import Q

from django.http import HttpResponse
from django.shortcuts import render
from django.utils.datastructures import OrderedSet
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

from .models import Championship, Game, Club, Change, Position


# Create your views here.

def show_rating(request):
    clubs = Club.objects.all().order_by('-rating')
    return render(request, 'EloMain/rating.html', locals())

def show_rating_by_champ(request, champ_id):
    clubs = Club.objects.filter(championship__id=champ_id).order_by('-rating')
    return render(request, 'EloMain/rating.html', locals())

def charts(request):
    return render(request, 'EloMain/charts.html')

def show_country_rating(request):
    tourns = Championship.objects.filter(elo_index=30)
    champs = []
    for champ in tourns:
        clubs = Club.objects.filter(championship=champ).order_by('-rating')
        clubs = clubs[:10]
        total = 0
        for club in clubs:
            total += club.rating
        champs.append((champ,round(total/10,2),'rating/{}'.format(champ.id)))
    champs.sort(key=lambda x: -x[1])

    print(champs)

    return render(request, 'EloMain/country_rating.html', locals())

def top_delta(request):
    changes = Change.objects.all().order_by('-rating_delta')
    changes = changes[:5]
    return render(request, 'EloMain/top_changes.html', locals())

def top_rating_ever(request):
    changes = Change.objects.all().order_by('-rating_after')
    used_clubs = []
    top = []
    i = 0
    while len(top)<5:
        change = changes[i]
        if change.club not in used_clubs:
            top.append(change)
            used_clubs.append(change.club)
        i+=1
    print(top)

    return render(request, 'EloMain/top_rating_ever.html', locals())

def get_chart(request):
    club_names = ('Ливерпуль','Бавария', 'Барселона')
    club_changes = Change.objects.filter(Q(club__name=club_names[0]) | Q(club__name=club_names[1]) | Q(club__name=club_names[2])).order_by('id')
    script = ''
    last_liv = 1000
    last_bav = 1000
    last_bars = 1000
    for change in club_changes:
        date = change.game.date
        if change.club.name==club_names[0]:
            script += '[new Date({},{},{}), {}, {}, {}],'.format(date.year,date.month,date.day,change.rating_after,last_bav, last_bars)
            last_liv = change.rating_after
        elif change.club.name == club_names[1]:
            script += '[new Date({},{},{}), {}, {}, {}],'.format(date.year, date.month, date.day, last_liv, change.rating_after, last_bars)
            last_bav = change.rating_after
        elif change.club.name == club_names[2]:
            script += '[new Date({},{},{}), {}, {}, {}],'.format(date.year, date.month, date.day, last_liv, last_bav ,change.rating_after)
            last_bars = change.rating_after
    print(script)
    return HttpResponse(script)

def fill_national(request):

    russian_champ = Championship.objects.get(name='Украина')
    russian_link = russian_champ.link

    # driver = webdriver.Chrome('/home/leonid/chromedriver_linux64/chromedriver')
    driver = webdriver.Chrome('/home/lenkov/disk/work/chromedriver_linux64/chromedriver')
    driver.get(russian_link)

    print(0)

    i = 1

    while len(driver.find_elements_by_xpath("//div[@class='live_comptt_bd' and ./div[@class='block_header' and text()='{}-й тур']]".format(i)))>0:
        print("Tour {}".format(i))
        matches = driver.find_elements_by_xpath("//div[@class='live_comptt_bd' and ./div[@class='block_header' and text()='{}-й тур']]//div[@class='game_block']//a".format(i))

        for match in matches:
            match_id = match.get_attribute('dt-id')
            date = match.find_element_by_xpath("//a[@dt-id={}]//div[@class='game_ht']//div[@class='game_start']//span".format(match_id)).text
            home_team = match.find_element_by_xpath("//a[@dt-id={}]//div[@class='game_ht']//div[@class='game_team']//span".format(match_id)).text
            home_score = match.find_element_by_xpath("//a[@dt-id={}]//div[@class='game_ht']//div[@class='game_goals']//span".format(match_id)).text
            away_score = match.find_element_by_xpath("//a[@dt-id={}]//div[@class='game_at']//div[@class='game_goals']//span".format(match_id)).text
            away_team = match.find_element_by_xpath("//a[@dt-id={}]//div[@class='game_at']//div[@class='game_team']//span".format(match_id)).text
            print("{} {} {}-{} {}".format(date,home_team,home_score,away_score,away_team))

            home_team_obj = Club.objects.get(name=home_team, championship=russian_champ)
            away_team_obj = Club.objects.get(name=away_team, championship=russian_champ)
            print(home_team)
            print(away_team)

            try:
                date1 = datetime.strptime(date, "%d.%m.%y")
            except Exception as e:
                print(e)
                continue

            game = Game(date=date1.strftime("%Y-%m-%d"), home_team=home_team_obj, away_team=away_team_obj, home_score=home_score, away_score=away_score, tournament=russian_champ)
            game.save()

        i+=1

    return HttpResponse(russian_champ.link)

def fill_lc(request):

    russian_champ = Championship.objects.get(name='Лига Чемпионов Группы')
    russian_link = russian_champ.link

    driver = webdriver.Chrome('/home/lenkov/disk/work/chromedriver_linux64/chromedriver')
    # driver = webdriver.Chrome('/home/leonid/chromedriver_linux64/chromedriver')

    driver.get(russian_link)

    print(0)

    i = 1

    # while i==1:
    while len(driver.find_elements_by_xpath("//div[@class='live_comptt_bd' and ./div[@class='block_header' and text()='Групповая стадия | {}-й тур']]".format(i)))>0:
        print("Tour {}".format(i))
        matches = driver.find_elements_by_xpath("//div[@class='live_comptt_bd' and ./div[@class='block_header' and text()='Групповая стадия | {}-й тур']]//div[@class='game_block']//a".format(i))
        print("len(matches)={}".format(len(matches)))
        for match in matches:
            match_id = match.get_attribute('dt-id')
            date = match.find_element_by_xpath("//a[@dt-id={}]//div[@class='game_ht']//div[@class='game_start']//span".format(match_id)).text
            home_team = match.find_element_by_xpath("//a[@dt-id={}]//div[@class='game_ht']//div[@class='game_team']//span".format(match_id)).text
            home_score = match.find_element_by_xpath("//a[@dt-id={}]//div[@class='game_ht']//div[@class='game_goals']//span".format(match_id)).text
            away_score = match.find_element_by_xpath("//a[@dt-id={}]//div[@class='game_at']//div[@class='game_goals']//span".format(match_id)).text
            away_team = match.find_element_by_xpath("//a[@dt-id={}]//div[@class='game_at']//div[@class='game_team']//span".format(match_id)).text
            print("{} {} {}-{} {}".format(date,home_team,home_score,away_score,away_team))

            home_team_obj = Club.objects.get(name=home_team)
            away_team_obj = Club.objects.get(name=away_team)
            print(home_team)
            print(away_team)

            date1 = datetime.strptime(date, "%d.%m.%y")

            game = Game(date=date1.strftime("%Y-%m-%d"), home_team=home_team_obj, away_team=away_team_obj, home_score=home_score, away_score=away_score, tournament=russian_champ)
            game.save()

        i+=1

    return HttpResponse(russian_champ.link)

def fill_lc_final(request):

    russian_champ = Championship.objects.get(name='Лига Европы Финалы')
    russian_link = russian_champ.link

    driver = webdriver.Chrome('/home/lenkov/disk/work/chromedriver_linux64/chromedriver')
    # driver = webdriver.Chrome('/home/leonid/chromedriver_linux64/chromedriver')
    driver.get(russian_link)

    print(0)


    finals = ('1/16 финала','1/8 финала','1/4 финала','1/2 финала','Четвертьфинал', 'Полуфинал','Финал')

    for final in finals:

        matches = driver.find_elements_by_xpath("//div[@class='live_comptt_bd' and ./div[@class='block_header' and text()='{}']]//div[@class='game_block']//a".format(final))
        print("len(matches)={}".format(len(matches)))
        for match in matches:
            match_id = match.get_attribute('dt-id')
            date = match.find_element_by_xpath("//a[@dt-id={}]//div[@class='game_ht']//div[@class='game_start']//span".format(match_id)).text
            home_team = match.find_element_by_xpath("//a[@dt-id={}]//div[@class='game_ht']//div[@class='game_team']//span".format(match_id)).text
            home_score = match.find_element_by_xpath("//a[@dt-id={}]//div[@class='game_ht']//div[@class='game_goals']//span".format(match_id)).text
            away_score = match.find_element_by_xpath("//a[@dt-id={}]//div[@class='game_at']//div[@class='game_goals']//span".format(match_id)).text
            away_team = match.find_element_by_xpath("//a[@dt-id={}]//div[@class='game_at']//div[@class='game_team']//span".format(match_id)).text
            print("{} {} {}-{} {}".format(date,home_team,home_score,away_score,away_team))

            home_team_obj = Club.objects.get(name=home_team)
            away_team_obj = Club.objects.get(name=away_team)
            print(home_team)
            print(away_team)

            date1 = datetime.strptime(date, "%d.%m.%y")

            game = Game(date=date1.strftime("%Y-%m-%d"), home_team=home_team_obj, away_team=away_team_obj, home_score=home_score, away_score=away_score, tournament=russian_champ)
            game.save()

    return HttpResponse(russian_champ.link)

def reset_changes(request):
    Change.objects.all().delete()
    return HttpResponse("Готово")

def reset_ratings(request):
    for club in Club.objects.all():
        club.rating = 1000
        club.save()
    return HttpResponse("Готово")

def reset_matches(requset):
    # Game.objects.filter(tournament__name='Голландия').delete()
    return HttpResponse("Готово")

def test_ratings(request):
    clubs = Club.objects.all()
    for club in clubs:
        changes = Change.objects.filter(club=club).order_by('game__date')
        i = 0
        while i < len(changes) - 1:
            assert changes[i].rating_after == changes[i + 1].rating_before
            i += 1

    return HttpResponse("Готово")

def calc(request):
    games = Game.objects.all().order_by('date')
    len_games = len(games)
    print("Количество: {}".format(len_games))
    # print(games[0], games[len_games-1])

    # return HttpResponse("Готово")

    # for i in range(2):
    #     game = games[i]
    for game in games:
        index = game.tournament.elo_index

        home_team = game.home_team
        away_team = game.away_team
        ht_score = game.home_score
        at_score = game.away_score

        ht_rating = home_team.rating
        at_rating = away_team.rating

        delta = calc_rating_delta(ht_rating,at_rating,ht_score,at_score,index)

        home_team.rating = ht_rating + delta
        away_team.rating = at_rating - delta

        home_team.save()
        away_team.save()

        change_h = Change(game=game, club=home_team, rating_before=ht_rating, rating_after=home_team.rating, rating_delta=delta)
        change_a = Change(game=game, club=away_team, rating_before=at_rating, rating_after=away_team.rating, rating_delta=-delta)

        change_h.save()
        change_a.save()

        print("{} {} - {} {}".format(home_team.name, home_team.rating, away_team.rating, away_team.name))

    clubs = Club.objects.all().order_by('-rating')

    return HttpResponse("Готово")

def calc_rating_delta(own_rating, rival_rating, own_score, rival_score, index):
    goals_delta = own_score - rival_score
    rating_delta = own_rating - rival_rating
    return round(index*calc_G(goals_delta)*(calc_W(goals_delta) - calc_We(rating_delta)),2)

def calc_G(goals_delta):
    goals_delta = abs(goals_delta)

    if goals_delta<2:
        return 1.0

    if goals_delta==2:
        return 1.5

    return (11+goals_delta)/8

def calc_We(rating_delta):
    power = -rating_delta/400
    return 1/(10**power + 1)

def calc_W(goals_delta):
    if goals_delta<0:
        return 0
    if goals_delta==0:
        return 0.5
    if goals_delta>0:
        return 1

def fill_change_position(request):
    dates = OrderedSet()
    for x in Change.objects.all().order_by('id'):
        if x.game.date not in dates:
            dates.add(x.game.date)

    for date in dates:
        changes = Change.objects.all().filter(game__date__lte=date).order_by('-rating_after').distinct()[:10]
        if len(changes)<10:
            continue

        print(type(changes[0].club))

        position = Position(date,changes[0].club,changes[1].club,changes[2].club,changes[3].club,changes[4].club,changes[5].club,changes[6].club,changes[7].club,changes[8].club,changes[9].club)
        print(position)
        position.save()



    return HttpResponse(dates)
