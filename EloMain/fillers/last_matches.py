from datetime import datetime

import requests
from bs4 import BeautifulSoup
from django.http import HttpResponse

from EloMain.calculator.rating_delta import calc_rating_delta
from EloMain.models import Championship, Game, Club, Change

from concurrent.futures import wait, ProcessPoolExecutor


class Stats:
    await_matches = 0
    counter = 0
    filter_date = None
    filter_date2 = None

    def __str__(self):
        return "{} {} {} {}".format(self.await_matches, self.counter, self.filter_date, self.filter_date2)

def fill_last_matches(request):
    champs = Championship.objects.all()

    date_str = '25.1.20'
    filter_date = datetime.strptime(date_str, "%d.%m.%y")
    date_str2 = '25.11.29'
    filter_date2 = datetime.strptime(date_str2, "%d.%m.%y")
    stats = Stats()
    stats.await_matches = 0
    stats.counter = 0
    stats.filter_date = filter_date
    stats.filter_date2 = filter_date2

    pool = ProcessPoolExecutor(16)
    futures = []
    for champ in champs:
        futures.append(pool.submit(fill_championship, champ,stats))

    wait(futures)

    return HttpResponse('Done')

def fill_championship(champ, stats):
    page_content = requests.get(champ.link).content
    page_soup = BeautifulSoup(page_content, 'html.parser')
    matches = page_soup.find_all(class_='game_block')

    for match in matches:
        date, ht_name, ht_score, at_score, at_name=find_match_data(match)
        print("{} {} {}-{} {}".format(date, ht_name, ht_score, at_score, at_name))
        if not validate_date(date):
            stats.await_matches+=1
            continue

        date_obj = get_date_from_string(date)
        if date_obj < stats.filter_date:
            break

        if date_obj > stats.filter_date2:
            break

        if not check_game_exist(date_obj,ht_name,at_name):
            home_team_obj = Club.objects.get(name=ht_name)
            away_team_obj = Club.objects.get(name=at_name)
            game = Game(date=date_obj.strftime("%Y-%m-%d"), home_team=home_team_obj, away_team=away_team_obj,
                        home_score=int(ht_score), away_score=int(at_score), tournament=champ)
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
            stats.counter += 1

    if stats.await_matches>0:
        print("В ожидании ({}): {}".format(champ.name, stats.await_matches))
    if stats.counter>0:
        print("Записано ({}): {}".format(champ.name, stats.counter))

def find_match_data(match):
    date = match.find(class_='status').find('span').get_text()

    ht = match.find(class_='ht')
    ht_name, ht_score = find_name_score(ht)

    at = match.find(class_='at')
    at_name, at_score = find_name_score(at)

    return date, ht_name, ht_score, at_score, at_name

def find_name_score(element):
    name = element.find(class_='name').find('span').get_text()
    score = element.find(class_='gls').get_text()
    return name, score

def validate_date(date):
    try:
        datetime.strptime(date, "%d.%m.%y")
        return True
    except Exception as e:
        print(e)
        return False

def get_date_from_string(date):
    return datetime.strptime(date, "%d.%m.%y")

def check_game_exist(date, home_team, away_team):
    return Game.objects.filter(date=date, home_team__name=home_team, away_team__name=away_team).exists()
