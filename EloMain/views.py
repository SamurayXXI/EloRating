from asyncio import sleep
from datetime import datetime, date
import operator

from django.db.models import Q
from collections import OrderedDict
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

def panel(request):
    return render(request, 'EloMain/panel.html')

def charts(request):
    return render(request, 'EloMain/charts.html')

def position_charts(request):
    return render(request, 'EloMain/position_charts.html')

def show_country_rating(request):
    tourns = Championship.objects.filter(elo_index=30)
    champs = []
    for champ in tourns:
        clubs = Club.objects.filter(championship=champ).order_by('-rating').filter(~Q(name='Москва'))
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

def month_rating(request):
    date1 = date.today()
    changes = Change.objects.all().filter(rating_after__gte=1100).filter(game__date__gte=date(date1.year,date1.month-1,1),
                                       game__date__lt=date(date1.year,date1.month,1))
    clubs = {}
    for change in changes:
        if not change.club in clubs:
            clubs[change.club] = change.rating_delta
        else:
            clubs[change.club] += change.rating_delta
    clubs = [(k,clubs[k]) for k in sorted(clubs, key=clubs.get, reverse=True)]
    print(clubs)
    # for club in clubs:
        # print(club.name, clubs[club])

    return render(request, 'EloMain/month_rating.html', locals())

def year_rating(request):
    year = 2019
    changes = Change.objects.all().filter(game__date__gte=date(year,1,1),
                                       game__date__lte=date(year,12,31))
    clubs = {}
    for change in changes:
        if not change.club in clubs:
            clubs[change.club] = change.rating_delta
        else:
            clubs[change.club] += change.rating_delta
    clubs = [(k,clubs[k]) for k in sorted(clubs, key=clubs.get, reverse=True)]
    print(clubs)
    # for club in clubs:
        # print(club.name, clubs[club])

    return render(request, 'EloMain/year_rating.html', locals())


def position_continuity(request):
    time = {}
    i = 0
    positions = Position.objects.filter(date__gte='2010-06-01').order_by('date')
    while i<len(positions)-1:
        if positions[i].club_1 == positions[i+1].club_1:
            if positions[i].club_1 not in time:
                time[positions[i].club_1] = positions[i+1].date - positions[i].date
            else:
                time[positions[i].club_1]+= positions[i+1].date - positions[i].date
        else:
            if positions[i].club_1 not in time:
                time[positions[i].club_1] = positions[i+1].date - positions[i].date - datetime.timedelta(days=1)
            else:
                time[positions[i].club_1]+= positions[i+1].date - positions[i].date - datetime.timedelta(days=1)
        i+=1

    time_sorted = sorted(time.items(), key=lambda kv: -kv[1])

    return render(request, 'EloMain/top_places.html', locals())

def get_position_chart(request):
    club_name = 'Реал Мадрид'
    string = ''
    first_places = []
    positions = Position.objects.all().order_by('date')
    for position in positions:
        if position.club_1 not in first_places:
            first_places.append(position.club_1)
        if position.club_1 == club_name:
            string += '[new Date({},{},{}), {}],'.format(position.date.year,position.date.month, position.date.day, 1)
        elif position.club_2 == club_name:
            string += '[new Date({},{},{}), {}],'.format(position.date.year,position.date.month, position.date.day, 2)
        elif position.club_3 == club_name:
            string += '[new Date({},{},{}), {}],'.format(position.date.year,position.date.month, position.date.day, 3)
        elif position.club_4 == club_name:
            string += '[new Date({},{},{}), {}],'.format(position.date.year,position.date.month, position.date.day, 4)
        elif position.club_5 == club_name:
            string += '[new Date({},{},{}), {}],'.format(position.date.year,position.date.month, position.date.day, 5)
        elif position.club_6 == club_name:
            string += '[new Date({},{},{}), {}],'.format(position.date.year,position.date.month, position.date.day, 6)
        elif position.club_7 == club_name:
            string += '[new Date({},{},{}), {}],'.format(position.date.year,position.date.month, position.date.day, 7)
        elif position.club_8 == club_name:
            string += '[new Date({},{},{}), {}],'.format(position.date.year,position.date.month, position.date.day, 8)
        elif position.club_10 == club_name:
            string += '[new Date({},{},{}), {}],'.format(position.date.year,position.date.month, position.date.day, 10)
        else:
            string += '[new Date({},{},{}), {}],'.format(position.date.year, position.date.month, position.date.day, 11)

    print(first_places)
    return HttpResponse(string)

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

def fill_last_matches(request):
    # driver = webdriver.Chrome('/Users/leonid/Documents/work/chromedriver')
    # driver = webdriver.Chrome('/home/leonid/chromedriver_linux64/chromedriver')
    # driver = webdriver.Chrome('/home/lenkov/disk/work/chromedriver_linux64/chromedriver')
    driver = webdriver.Chrome('/home/dl/chromedriver_linux64/chromedriver')

    log = ''
    counter = 0
    date_str = '9.12.19'
    filter_date = datetime.strptime(date_str, "%d.%m.%y")

    date_str2 = '25.11.29'
    filter_date2 = datetime.strptime(date_str2, "%d.%m.%y")

    champs = Championship.objects.all()
    for champ in champs:

        driver.get(champ.link)

        def check_enter(driver):
            enter = driver.find_elements_by_xpath("//div[@class='live_comptt_bd']//div[@class='game_block']//a")
            print("len enter {}".format(len(enter)))
            return len(enter) > 7

        WebDriverWait(driver, 15, 0.1).until(check_enter)
        sleep(0.5)
        
        matches = driver.find_elements_by_xpath(
            "//div[@class='live_comptt_bd']//div[@class='game_block']//a")
        for match in matches:
            try:
                match_id = match.get_attribute('dt-id')
                date = match.find_element_by_xpath("//a[@dt-id={}]//div[@class='game_ht']//div[@class='game_start']//span".format(match_id)).text
                home_team = match.find_element_by_xpath("//a[@dt-id={}]//div[@class='game_ht']//div[@class='game_team']//span".format(match_id)).text
                home_score = match.find_element_by_xpath("//a[@dt-id={}]//div[@class='game_ht']//div[@class='game_goals']//span".format(match_id)).text
                away_score = match.find_element_by_xpath("//a[@dt-id={}]//div[@class='game_at']//div[@class='game_goals']//span".format(match_id)).text
                away_team = match.find_element_by_xpath("//a[@dt-id={}]//div[@class='game_at']//div[@class='game_team']//span".format(match_id)).text
            except Exception as e:
                print(e)
                continue

            print("{} {} {}-{} {}".format(date, home_team, home_score, away_score, away_team))


            try:
                date1 = datetime.strptime(date, "%d.%m.%y")
            except Exception as e:
                print(e)
                continue

            if date1 < filter_date:
                break

            if date1 > filter_date2:
                break

            if not Game.objects.filter(date=date1, home_team__name=home_team, away_team__name=away_team).exists():
                home_team_obj = Club.objects.get(name=home_team)
                away_team_obj = Club.objects.get(name=away_team)
                game = Game(date=date1.strftime("%Y-%m-%d"), home_team=home_team_obj, away_team=away_team_obj,
                            home_score=int(home_score), away_score=int(away_score), tournament=champ)
                game.save()

                index = game.tournament.elo_index

                home_team = game.home_team
                away_team = game.away_team
                ht_score = game.home_score
                at_score = game.away_score

                ht_rating = home_team.rating
                at_rating = away_team.rating

                delta = calc_rating_delta(ht_rating, at_rating, ht_score, at_score, index)

                home_team.rating = ht_rating + delta
                away_team.rating = at_rating - delta

                home_team.save()
                away_team.save()

                change_h = Change(game=game, club=home_team, rating_before=ht_rating, rating_after=home_team.rating,
                                  rating_delta=delta)
                change_a = Change(game=game, club=away_team, rating_before=at_rating, rating_after=away_team.rating,
                                  rating_delta=-delta)

                change_h.save()
                change_a.save()
                print("Save")
                counter += 1


    print("Добавлено {} матчей".format(counter))

    return HttpResponse('Done')

def fill_national(request):

    russian_champ = Championship.objects.get(name='Австрия')
    russian_link = russian_champ.link

    driver = webdriver.Chrome('/Users/leonid/Documents/work/chromedriver')
    # driver = webdriver.Chrome('/home/leonid/chromedriver_linux64/chromedriver')
    # driver = webdriver.Chrome('/home/lenkov/disk/work/chromedriver_linux64/chromedriver')
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

    russian_champ = Championship.objects.get(name='Лига Европы Группы')
    russian_link = russian_champ.link

    driver = webdriver.Chrome('/Users/leonid/Documents/work/chromedriver')
    # driver = webdriver.Chrome('/home/lenkov/disk/work/chromedriver_linux64/chromedriver')
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
    return round(index*calc_G(goals_delta)*(calc_W(goals_delta) - calc_We(rating_delta)),0)

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
    all_changes = Change.objects.all().order_by('-id')
    clubs = Club.objects.all().order_by('-rating')
    rating_list = [[x.name,x.rating] for x in clubs]
    last_club_list = tuple([x.name for x in clubs][:10])
    for change in all_changes:
        print(change.game.date)
        rating_record = next(x for x in rating_list if x[0] == change.club.name)
        rating_record[1] = change.rating_after
        rating_list.sort(key=lambda x: -x[1])
        club_list = tuple([x[0] for x in rating_list][:10])

        if club_list!=last_club_list:
            print("club list {}".format(club_list))
            print("Save")
            position = Position()
            position.date = change.game.date
            position.club_1 = club_list[0]
            position.club_2 = club_list[1]
            position.club_3 = club_list[2]
            position.club_4 = club_list[3]
            position.club_5 = club_list[4]
            position.club_6 = club_list[5]
            position.club_7 = club_list[6]
            position.club_8 = club_list[7]
            position.club_9 = club_list[8]
            position.club_10 = club_list[9]

            position.save()

            last_club_list = club_list

    return HttpResponse(dates)
