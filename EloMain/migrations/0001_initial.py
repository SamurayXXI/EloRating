# Generated by Django 2.2.7 on 2019-11-08 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Championship",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=30, verbose_name="Название")),
                ("icon", models.ImageField(upload_to="", verbose_name="Иконка")),
                ("link", models.TextField(verbose_name="Ссылка на матчи")),
                ("elo_index", models.IntegerField(verbose_name="Коэффициент рейтинга")),
            ],
            options={"verbose_name": "Чемпионат", "verbose_name_plural": "Чемпионаты", "db_table": "championships",},
        ),
        migrations.CreateModel(
            name="Club",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=50, verbose_name="Название")),
                ("logo", models.ImageField(upload_to="", verbose_name="Логотип")),
                ("rating", models.IntegerField(verbose_name="Рейтинг")),
            ],
            options={"verbose_name": "Клуб", "verbose_name_plural": "Клубы", "db_table": "clubs",},
        ),
    ]
