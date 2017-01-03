# djangular-bucketlist-app
[![Build Status](https://travis-ci.org/gitgik/djangular-bucketlist-app.svg?branch=master)](https://travis-ci.org/gitgik/djangular-bucketlist-app) [![Coverage Status](https://coveralls.io/repos/github/gitgik/djangular-bucketlist-app/badge.svg?branch=develop)](https://coveralls.io/github/gitgik/djangular-bucketlist-app?branch=develop) [![License](http://img.shields.io/:license-mit-blue.svg)](http://doge.mit-license.org)
A Django-powered Bucketlist API with an AngularJS consumption client.

## Technologies used
* [Django](https://www.djangoproject.com/): The web framework for perfectionists with deadlines (Django builds better web apps with less code).
* [Django Rest Framwork](http://www.django-rest-framework.org/): A powerful and flexible toolkit for building web APIs.
* [Swagger](http://swagger.io/): The world's most popular framework for documenting APIs.
* [AngularJS](https://angularjs.org/): The go-to framework for building HTML enhanced web apps.
* [Angular Material](https://material.angularjs.org/latest/): AngularJS implementation for Google's material design specification.
* [Google Web Fonts](https://www.google.com/fonts): Beautiful fonts from Google to complement your web app.
* Minor dependencies can be found in the requirements.txt file on the root folder.


## Installation
* If you wish to run your own build, first ensure you have python globally installed in your computer. If not, you can get python [here](https://www.python.org").
* After this, ensure you have installed virtualenv globally as well. If not, run this:
    ```
        $ pip install virtualenv
    ```
* Git clone this repo to your PC
    ```
        $ git clone https://github.com/gitgik/djangular-bucketlist-app.git
    ```


* #### Dependencies
    1. Cd into your the cloned repo as such:
        ```
        $ cd djangular-bucketlist-app
        ```

    2. Create and fire up your virtual environment:
        ```
        $ virtualenv env
        $ source env/bin/activate
        ```
    3. Install the django dependencies needed to run the app:
        ```
        $ pip install -r requirements.txt
        ```
    4. Install the bower components for the angularJS client
        ```
        $ bower install
        ```


* #### Collecting Static Files
    To collect all your static files for django to easily access them from one folder, simply do:
    ```
    $ python manage.py collectstatic --noinput
    ```

* #### Running It
    On your terminal, run the server using this one simple command:
    ```
    $ python manage.py runserver
    ```
    You can now access the bucketlist service on your browser by using
    ```
      http://localhost:8000/
    ```

## Todo
* Integrate Oauth for authenication.
* Use angular 2.0 on the consumption client.
* Add voice command functionality :-D
