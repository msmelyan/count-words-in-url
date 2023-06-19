from flask import Flask, request, render_template
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def count_words():
    count = None

    if request.method == 'POST':
        url = request.form.get('url')

        try:
            r = requests.get(url)
        except requests.exceptions.RequestException as e:
            return render_template('index.html', error="Invalid URL or the site is currently inaccessible.")
        
        soup = BeautifulSoup(r.text, 'html.parser')
        words = re.findall(r'\w+', soup.get_text())
        count = len(words)

    return render_template('index.html', count=count)

if __name__ == '__main__':
    app.run(debug=True)

