# Generated by Django 2.2.7 on 2019-12-03 10:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('EloMain', '0010_auto_20191203_1013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='club',
            name='championship',
            field=models.ForeignKey(default=-1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='championship', to='EloMain.Championship', verbose_name='Чемпионат'),
        ),
    ]
