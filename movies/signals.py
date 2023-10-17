from pymongo import MongoClient
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime, timedelta

from .models import Movie

@receiver(post_save, sender=Movie)
def replicate_to_mongodb(sender, instance, **kwargs):
    # Create a MongoDB connection
    client = MongoClient('localhost', 27017)
    mongodb = client['your_mongodb_db']

    # Create a MongoDB collection for your model
    collection = mongodb['your_mongodb_collection']

    # Convert Django model data to a dictionary and insert it into MongoDB
    data_to_insert = instance.__dict__
    del data_to_insert['_state']  # Remove unnecessary metadata
    collection.insert_one(data_to_insert)


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
