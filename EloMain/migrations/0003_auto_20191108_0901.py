# Generated by Django 2.2.7 on 2019-11-08 09:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("EloMain", "0002_auto_20191108_0831"),
    ]

    operations = [
        migrations.AddField(
            model_name="club",
            name="championship",
            field=models.ForeignKey(
                default=-1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="championship",
                to="EloMain.Championship",
                verbose_name="Чемпионат",
            ),
        ),
        migrations.AlterField(
            model_name="championship",
            name="icon",
            field=models.ImageField(blank=True, null=True, upload_to="", verbose_name="Иконка"),
        ),
        migrations.AlterField(
            model_name="club",
            name="logo",
            field=models.ImageField(blank=True, null=True, upload_to="", verbose_name="Логотип"),
        ),
    ]
