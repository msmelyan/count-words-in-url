# Intro

This repo contains python code to implement a website which accepts webpage link and returns number of tokesn on that page. It is implemented using two processes:
* 
* web: a web server implemented in Flask, which prompts for the html link, calls a background worker which computes number of words on that page
* worker: a background process which accepts html link and computes number of words on the page, located at that link

Note that web and worker processes communicate via Heroku managed reddis queue.



# Deployment on Heroku

Create Heroku [account](https://signup.heroku.com/), if you do not have one yet.

Download and install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-command-line).



Clone the repository
Use Git to clone count-words-in-url's source code to your local machine.
```
git clone https://github.com/msmelyan/count-words-in-url.git
cd count-words-in-url
```

Direcotry contains web/ and worker/ subdirectory which implements corresponding processes. There is also Procfile in the root directory that specifies the commands to deploy processes. Those processes get compiled into Heroku containers, known as dynos.

Log in to your Heroku account and follow the prompts.
```
$ heroku login
```

Make some changes to the code you just cloned, if desired, and commit them
```
git add .
git commit -am "make it better"
```

Compile and deploy them to Heroku using Git.
```
# create application
heroku create count-words-in-url

# point to remote heroku repository
heroku git:remote -a count-words-in-url

# compile code heroku dynos (containers)
git push heroku main

# deploy redis
heroku addons:create heroku-redis

# deploy both dynos on a single Heroku instance each
heroku ps:scale web=1 worker=1 -a count-words-in-url 
```

When you are done, you can destroy application, as follows
```
heroku apps:destroy --app count-words-in-url --confirm count-words-in-url
```
