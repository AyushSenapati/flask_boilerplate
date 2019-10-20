## Flask-Boilerplate
- It provides directory structure to build multi-service based monolithic Flask Restful application.
- Application is structured such a way that, services could be detached to build microservices.

## Boilerplate usage

Run below command to create a virtualenv
```
$ virtualenv -p python3.7 flask-api
$ cd flask-api
$ source bin/activate
$ mkdir src
$ cd !!:1
$ git clone https://github.com/AyushSenapati/flask_boilerplate.git .
$ pip install -r requirements.txt
```
Above commands sets up the dev environment.
Now to run the application run any of the below commands:
```
$ export FLASK_ENV=development
$ flask run
```
OR
```
$ export FLASK_ENV=development
$ python manage.py run
```
Now to scaffhold services, you can use the provided bootstrap_service script.
```
$ cd app
$ python bootstrap_service.py
Service Name: test
About to create a service with name: service_test
Confirm? (y/N): y
        services/service_test/controllers/ created.
        services/service_test/models/ created.
        services/service_test/tests/ created.
        services/service_test/custom_exceptions/ created.
        services/service_test/__init__.py created
        services/service_test/urls.py created
NOTE: Add the service: 'service_test' to the INSTALLED_SERVICES in the settings file
```
This script creates the service under services directory.


As mentioned in the output, you need to add the created service name to the INSTALLED_SERVICES list present in the base.py module inside the settings directory. It will automatically register the service blueprint to the Flask app.

Now you can add controllers for the service and list the routes in urls.py module.

Below command will show all the routes registered to the Flask application.
```
$ python manage.py routes
```