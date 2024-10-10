# backend/tasks/backup.py
from celery import shared_task
from backend.RestaurantLeaderboard import Leaderboard
from backend.models import Leaderborad_backup
import logging

# Set up logging
logger = logging.getLogger(__name__)

# @shared_task
# def my_function():
#     logger.info("executed")
    

@shared_task
def my_function():
    # Initialize the Leaderboard object
    leaderboard = Leaderboard()
    
    # Fetch the top 10 restaurants
    top_restaurants = leaderboard.get_all_scores()
    
    for restaurant_id, score in top_restaurants:
        # Decode the byte string for restaurant_id if necessary
        if isinstance(restaurant_id, bytes):
            restaurant_id = restaurant_id.decode('utf-8')

        # Update or create the leaderboard backup entry
        Leaderborad_backup.objects.update_or_create(
            restaurant_name=restaurant_id,  # Lookup field(s)
            defaults={'score': score}
        )
        logger.info(f"Fetched restaurants data:{restaurant_id} {score}")


