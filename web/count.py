from flask import Flask, request, render_template
import requests
import re, os, sys
import redis
from rq import Worker, Queue, Connection

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

app = Flask(__name__)
redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
conn = redis.from_url(redis_url)
# create a RQ queue:
q = Queue(connection=conn)

def count_words_in_url(url):
    #resp = requests.get(url)
    #print (resp.text.split())
    try:
        r = requests.get(url)
    except requests.exceptions.RequestException as e:
        return render_template('index.html', error="Invalid URL or the site is currently inaccessible.")
    return len(r.text.split())

@app.route('/', methods=['GET', 'POST'])
def index():
    count = None

    if request.method == 'POST':
        url = request.form.get('url')
        # count = count_words_in_url(url)
        job = q.enqueue('web.count.count_words_in_url', url)
        count = job.result
    
    return render_template('index.html', count=count)

if __name__ == '__main__':
    app.run(debug=True)

