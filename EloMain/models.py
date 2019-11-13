from django.db import models

# Create your models here.
class Championship(models.Model):
    class Meta:
        db_table = 'championships'
        verbose_name = 'Чемпионат'
        verbose_name_plural = 'Чемпионаты'

    name = models.CharField(max_length=30, verbose_name='Название')
    icon = models.ImageField(verbose_name='Иконка', null=True, blank=True)
    link = models.TextField(verbose_name='Ссылка на матчи')
    elo_index = models.IntegerField(verbose_name='Коэффициент рейтинга')

    def __str__(self):
        return self.name

class Club(models.Model):
    class Meta:
        db_table = 'clubs'
        verbose_name = 'Клуб'
        verbose_name_plural = 'Клубы'

    name = models.CharField(max_length=50, verbose_name='Название')
    logo = models.ImageField(verbose_name='Логотип', null=True, blank=True)
    rating = models.IntegerField(verbose_name='Рейтинг')
    championship = models.ForeignKey(Championship, on_delete=models.CASCADE, related_name='championship', verbose_name='Чемпионат', default=-1)

    def __str__(self):
        return self.name

class Game(models.Model):
    class Meta:
        db_table = 'games'
        verbose_name = 'Игра'
        verbose_name_plural = 'Игры'

    date = models.DateField(verbose_name='Дата')
    tournament = models.ForeignKey(Championship, on_delete=models.CASCADE, related_name='tournament', verbose_name='Турнир', default=-1)
    home_team = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='home_team', verbose_name='Хозяева')
    away_team = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='away_team', verbose_name='Гости')
    home_score = models.IntegerField(verbose_name='Забили хозяева')
    away_score = models.IntegerField(verbose_name='Забили гости')

    def __str__(self):
        return "{} {} {}-{} {}".format(self.date, self.home_team, self.home_score, self.away_score, self.away_team)

class Change(models.Model):
    class Meta:
        db_table = 'changes'
        verbose_name = 'Изменение рейтинга'
        verbose_name_plural = 'Изменения рейтинга'

    game = models.ForeignKey(Game, on_delete=models.DO_NOTHING, related_name='game', verbose_name='Игра')
    club = models.ForeignKey(Club, on_delete=models.DO_NOTHING, related_name='club', verbose_name='Клуб')
    rating_before = models.IntegerField(verbose_name='Рейтинг до')
    rating_after = models.IntegerField(verbose_name='Рейтинг после')
    rating_delta = models.IntegerField(verbose_name='Дельта')

    def __str__(self):
        return "{} {} {}".format(self.game.date,self.club.name,self.rating_delta)

class Position(models.Model):
    class Meta:
        db_table = 'positions'
        verbose_name = 'Место рейтинга'
        verbose_name_plural = 'Места рейтинга'

    date = models.DateField(verbose_name='Дата')
    club_1 = models.CharField(max_length=50, verbose_name='1-е место')
    club_2 = models.CharField(max_length=50, verbose_name='2-е место')
    club_3 = models.CharField(max_length=50, verbose_name='3-е место')
    club_4 = models.CharField(max_length=50, verbose_name='4-е место')
    club_5 = models.CharField(max_length=50, verbose_name='5-е место')
    club_6 = models.CharField(max_length=50, verbose_name='6-е место')
    club_7 = models.CharField(max_length=50, verbose_name='7-е место')
    club_8 = models.CharField(max_length=50, verbose_name='8-е место')
    club_9 = models.CharField(max_length=50, verbose_name='9-е место')
    club_10 = models.CharField(max_length=50, verbose_name='10-е место')


    def __str__(self):
        return "{} {} {} {} {} {} {} {} {} {} {}".format(self.date,self.club_1,self.club_2,self.club_3,self.club_4,self.club_5,self.club_6,self.club_7,self.club_8,self.club_9,self.club_10)
