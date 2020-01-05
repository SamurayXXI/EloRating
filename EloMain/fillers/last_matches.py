from datetime import datetime
from asyncio import sleep

from django.http import HttpResponse
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

from EloMain.calculator.rating_delta import calc_rating_delta
from EloMain.models import Championship, Game, Club, Change


def fill_last_matches(request):
    # driver = webdriver.Chrome('/Users/leonid/Documents/work/chromedriver')
    driver = webdriver.Chrome('/home/leonid/chromedriver_linux64/chromedriver')
    # driver = webdriver.Chrome('/home/lenkov/disk/work/chromedriver_linux64/chromedriver')
    # driver = webdriver.Chrome('/home/dl/chromedriver_linux64/chromedriver')

    log = ''
    counter = 0
    await_matches = 0
    date_str = '3.1.20'
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
                date = match.find_element_by_xpath("//a[@dt-id={}]//div[@class='status']//span".format(match_id)).text
                home_team = match.find_element_by_xpath(
                    "//a[@dt-id={}]//div[@class='ht']//div[@class='name']//span".format(match_id)).text
                home_score = match.find_element_by_xpath(
                    "//a[@dt-id={}]//div[@class='ht']//div[@class='gls']".format(match_id)).text
                away_score = match.find_element_by_xpath(
                    "//a[@dt-id={}]//div[@class='at']//div[@class='gls']".format(match_id)).text
                away_team = match.find_element_by_xpath(
                    "//a[@dt-id={}]//div[@class='at']//div[@class='name']//span".format(match_id)).text
            except Exception as e:
                print(e)
                continue

            print("{} {} {}-{} {}".format(date, home_team, home_score, away_score, away_team))

            try:
                date1 = datetime.strptime(date, "%d.%m.%y")
            except Exception as e:
                print(e)
                await_matches += 1
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

    print("Добавлено матчей: {}".format(counter))
    print("Матчей в обработке: {}".format(await_matches))

    return HttpResponse('Done')
