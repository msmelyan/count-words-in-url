import re, os, sys, time
from flask import Flask, request, render_template
import requests
import redis
from rq import Worker, Queue, Connection
from rq.job import Job
from rq.exceptions import NoSuchJobError

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
        while True:
            try:
                # Re-fetch the job to get updated status and result
                job.refresh()
                
                if job.is_finished:
                    # If the job is finished, its result is ready and can be used
                    count = job.result
                    break
                else:
                    # If the job is not finished, wait for a bit before checking again
                    time.sleep(1)
            except NoSuchJobError:
                # The job does not exist, possibly because it's already finished and its data was expired
                break  
        print('count = ', count)
        
    return render_template('index.html', count=count)

if __name__ == '__main__':
    app.run(debug=True)

