import redis
from django.conf import settings

class Leaderboard:
    def __init__(self, name="-"):
        try:
            # Attempt to connect to Redis
            self.redis_client = redis.StrictRedis.from_url(settings.CACHES['default']['LOCATION'])
            self.name = name
        except redis.ConnectionError as e:
            # Handle specific redis connection errors
            print(f"Redis connection error: {e}")
            self.redis_client = None
            return 
        except Exception as e:
            # Handle any other exceptions
            print(f"An error occurred in Leaderboard initialization: {e}")
            self.redis_client = None
            return

    def update_score(self, restaurant_name, score_delta):
        """Update the score of a restaurant based on sentiment analysis."""
        print("excuted")
        self.redis_client.zadd(self.name,{restaurant_name: score_delta})

    def get_rank(self, restaurant_name):
        """Get the rank of a restaurant (1-based)."""
        rank = self.redis_client.zrevrank(self.name, restaurant_name)
        return rank + 1 if rank is not None else None

    def get_score(self, restaurant_id):
        """Get the score of a restaurant."""
        return self.redis_client.zscore(self.name, restaurant_id)

    def get_top_n(self, n=10):
        """Retrieve the top N restaurants."""
        return self.redis_client.zrevrange(self.name, 0, n - 1, withscores=True)

    def get_bottom_n(self, n=10):
        """Retrieve the bottom N restaurants."""
        return self.redis_client.zrange(self.name, 0, n - 1, withscores=True)
    
    def get_all_scores(self):
        """Retrieve all restaurants and their scores."""
        return self.redis_client.zrange(self.name, 0, -1, withscores=True)