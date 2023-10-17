from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _



STATUS_CHOICES = [
    _(('coming-up', 'Coming Up')),
    _(('starting', 'Starting')),
    _(('running', 'Running')),
    _(('finished', 'Finished')),
]

class Movie(models.Model):
    name = models.CharField(max_length=120)
    protagonist = models.CharField(max_length=50)
    poster = models.ImageField()
    start_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='coming-up')
    ranking = models.IntegerField(default=0, db_index=True)
    
    