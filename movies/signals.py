from pymongo import MongoClient
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime, timedelta
from .mongo import mongo_db

from .models import Movie

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Movie



@receiver(post_save, sender=Movie)
def sync_movie_to_mongodb(sender, instance, created, **kwargs):
    if created:
        print("Instance has been saved to Mongo db")
        movie_data = {
            'name': instance.name,
            'protagonist': instance.protagonist,
            'status': instance.status,
            'start_date': instance.start_date,
            'ranking': instance.ranking,
        }
        mongo_db.movies.insert_one(movie_data)
    else:
        pass



@receiver(post_delete, sender=Movie)
def delete_movie_from_mongodb(sender, instance, **kwargs):
    mongo_db.movies.delete_one({"id": instance.id})



@receiver(post_save, sender=Movie)
def update_ranking(sender, instance, created, **kwargs):
    if created and instance.status == 'upcoming':
        time_elapsed = datetime.now() - instance.created
        minutes_elapsed = time_elapsed.total_seconds() / 60
        intervals = minutes_elapsed // 5
        instance.ranking = 10 * intervals
        instance.save()
