[![Build Status](https://travis-ci.org/andela-mochieng/PimpPic.svg?branch=fb)](https://travis-ci.org/andela-mochieng/PimpPic)
[![Coverage Status](https://coveralls.io/repos/github/andela-mochieng/PimpPic/badge.svg?branch=fb)](https://coveralls.io/github/andela-mochieng/PimpPic?branch=fb)
## Picfront Image Editing web app


  This app allows you to upload images, add filters to them and share on facebook.It consists of a django Rest API and a frontend built with ng2. 

# Dependencies:
###Backend dependencies:
    Django - The backbone upon which this REST API is built upon. It's a Python web framework that features models, views, url routes and user management among many other features.

    Django REST framework - This is a powerful and flexible toolkit for building browsable REST APIs. It includes support for model serialization, permissions (default and custom) and viewsets among other features.

    Pillow - Python Image Manipulation Library
###Frontend dependencies:
 
    Materialize CSS - The front end framework from which all the elements and controls on the front end have been created.

    ng2 - Is a JS front end MVC (MVVM?) framework

# Features:
*  Log in with facebook.
*  A user can Upload images.
*  Then apply filters on them images.
*  A user can download the edited image.
*  A user can logout.

## Usage:

* Clone the repo: `$ git clone https://github.com/andela-mochieng/PimpPic.git`

* Install requirements.
 ` $ pip install -r requirements.txt`

* Create a .env.yml file in the root of PimpPic with the following settings (shown settings are samples)

    ```
    DB_USER: 'Administrator'

    DB_PASSWORD: 'administrator'

    SECRET_KEY: 'your-secret'

    SOCIAL_AUTH_LOGIN_REDIRECT_URL: '/#/account/'

    SOCIAL_AUTH_LOGIN_URL: '/'

    SOCIAL_AUTH_FACEBOOK_KEY: 'your-facebook-key'

    SOCIAL_AUTH_FACEBOOK_SECRET: 'your-facebook-secret'
    ```

* Install the project's database. This project uses PostgreSQL.

* Install frontend dependencies as described in the package.json file.
* After installation, create a database on PostgreSQL for this app.
* Perform database migrations.
    `python manage.py makemigrations `
    `python manage.py migrate `

* Run the application
 `python manage.py runserver`


## Testing
To run tests: `$ coverage run --source=pic manage.py test` then: `$ coverage report -m` 