import sys,os
import redis
from rq import Worker, Queue, Connection

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from web.count import count_words_in_url

listen = ['high', 'default', 'low']

redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')

conn = redis.from_url(redis_url)

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(map(Queue, listen))
        worker.work()
