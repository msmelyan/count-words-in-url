# Intro

This repo contains python code to implement a website which accepts webpage link and returns number of tokesn on that page. It is implemented using two processes:
* 
* web: a web server implemented in Flask, which prompts for the html link, calls a background worker which computes number of words on that page
* worker: a background process which accepts html link and computes number of words on the page, located at that link

Note that web and worker processes communicate via Heroku managed reddis queue.



# Deployment on Heroku

Create Heroku [account](https://signup.heroku.com/), if you do not have one yet.

Download and install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-command-line).

Log in to your Heroku account and follow the prompts.
```
$ heroku login
```

Clone the repository
Use Git to clone count-words-in-url's source code to your local machine.
```
$ heroku git:clone -a count-words-in-url
$ cd count-words-in-url
```

Direcotry contains web/ and worker/ subdirectory which implements corresponding processes. There is also Procfile in the root directory that specifies the commands to deploy processes. Those processes get compiled into Heroku containers, known as dynos.

Compiler both pro
Make some changes to the code you just cloned and deploy them to Heroku using Git.
```
$ git add .
$ git commit -am "make it better"
$ heroku create count-words-in-url # create application
$ git push heroku main  # compile into heroku dynos (containers)
$ heroku git:remote -a count-words-in-url
$ heroku addons:create heroku-redis # deploy redis
$ heroku ps:scale web=1 worker=1 -a count-words-in-url # deploy both dynos on a single Heroku instance each
```

