# Generated by Django 2.2.7 on 2019-12-03 10:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('EloMain', '0011_auto_20191203_1014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='club',
            name='championship',
            field=models.ForeignKey(default=-1, on_delete=django.db.models.deletion.CASCADE, related_name='championship', to='EloMain.Championship', verbose_name='Чемпионат'),
        ),
        migrations.AlterField(
            model_name='game',
            name='away_team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='away_team', to='EloMain.Club', verbose_name='Гости'),
        ),
        migrations.AlterField(
            model_name='game',
            name='home_team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='home_team', to='EloMain.Club', verbose_name='Хозяева'),
        ),
    ]