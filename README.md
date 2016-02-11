# djangular-bucketlist-app [![Build Status](https://travis-ci.org/andela-ggikera/djangular-bucketlist-app.svg?branch=master)](https://travis-ci.org/andela-ggikera/djangular-bucketlist-app)
A Django-powered Bucketlist API with an AngularJS consumption client

## Technologies used
* [Django](https://www.djangoproject.com/): The web framwork for perfectionists with deadlines (builds better web apps with less code).
* [Django Rest Framwork](http://www.django-rest-framework.org/): A powerful and flexible toolkit for building APIs.
* [Swagger](http://swagger.io/): The worlds most popular framework for documenting APIs.
* [AngularJS](https://angularjs.org/): HTML enhanced web apps framework.
* [Angular Material](https://material.angularjs.org/latest/): Angular's implementation for Google's material design specification.
* [Google Web Fonts](https://www.google.com/fonts): Beautiful fonts from Google to complement your web app.


## Installation
* If you wish to run your own build, first ensure you have python globally installed in your computer. If not, you can get python [here](https://www.python.org").
* After this, ensure you have installed virtualenv globally as well. If not, run this:
``` $ pip install virtualenv```
* Git clone this repo to your PC
    ```$ git clone https://github.com/andela-ggikera/djangular-bucketlist-app.git```


* #### Dependencies
    1. Cd into your the cloned repo as such:
        ```$ cd djangular-bucketlist-app```

    2. Create and fire up your virtual environment:
        ```
        $ virtualenv env
        $ source env/bin/activate
        ```
    3. Install the dependencies needed to run the app:
        ```$ pip install -r requirements.txt```
        ```$ bower install```


* #### Run It
    Fire the engines using this one simple command:
        ```$ python manage.py runserver```
    You can now access the bucketlist service on your browser by using ``` http://localhost:8000/```.

## Todo
* Integrate Oauth for authenication.
* Use angular 2.0 on the consumption client.
* Add voice command functionality :-D

