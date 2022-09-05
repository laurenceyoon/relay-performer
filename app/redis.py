import redis

pool = redis.ConnectionPool(host="localhost", port=6379, db=0)
redis_client = redis.Redis(connection_pool=pool)
