# Generated by Django 2.2.7 on 2019-12-03 10:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("EloMain", "0009_auto_20191113_1041"),
    ]

    operations = [
        migrations.AlterField(
            model_name="game",
            name="away_team",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="away_team",
                to="EloMain.Club",
                verbose_name="Гости",
            ),
        ),
        migrations.AlterField(
            model_name="game",
            name="home_team",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="home_team",
                to="EloMain.Club",
                verbose_name="Хозяева",
            ),
        ),
    ]
