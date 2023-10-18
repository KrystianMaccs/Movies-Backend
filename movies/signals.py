from pymongo import MongoClient
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime, timedelta

from .models import Movie

from django.db.models.signals import post_save, post_delete, post_update
from django.dispatch import receiver
from .models import Movie



@receiver(post_save, sender=Movie)
def sync_movie_to_mongodb(sender, instance, created, **kwargs):
    if created:
        print("Instance has been saved to Mongo db")
        mongo_db.movies.insert_one(instance.to_mongo())
    else:
        mongo_db.movies.update_one({"id": instance.id}, {"$set": instance.to_mongo()})


@receiver(post_delete, sender=Movie)
def delete_movie_from_mongodb(sender, instance, **kwargs):
    mongo_db.movies.delete_one({"id": instance.id})



@receiver(post_save, sender=Movie)
def update_ranking(sender, instance, created, **kwargs):
    if created and instance.status == 'upcoming':
        # Calculate the number of 5-minute intervals since creation
        time_elapsed = datetime.now() - instance.created
        minutes_elapsed = time_elapsed.total_seconds() / 60
        intervals = minutes_elapsed // 5

        # Update the ranking by increasing it by 10 for each interval
        instance.ranking = 10 * intervals
        instance.save()
