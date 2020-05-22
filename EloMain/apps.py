from django.apps import AppConfig


class EloMainConfig(AppConfig):
    name = "EloMain"

    def ready(self):
        from .models import Championship
        from EloRating.celery import app
        from celery.schedules import crontab
        app.conf.beat_schedule = {}
        for champ in Championship.objects.all():
            def schedule(champ_id):
                app.conf.beat_schedule[f'fill-championship-{champ_id}'] = {
                    'task': 'EloMain.tasks.fill_championship',
                    'schedule': crontab(minute=0, hour=4),
                    'args': (champ_id,)
                }
            schedule(champ.id)
