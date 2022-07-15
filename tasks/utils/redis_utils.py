import redis
import os
import json

class Client():
    def __init__(self):
        self.r = redis.from_url(os.environ.get("REDIS_URL"))

    def get(self, k):
        val = self.r.get(k)
        return json.loads(val) if val else None

    def set(self, k, v):
        self.r.set(k, json.dumps(v))
