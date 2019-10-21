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

A template of dockerfile is provided with this boilerplate. To build image using this template, first rename it to dockerfile and do any modifications needed, then run following command being in the project root directory.

```
$ docker build -t flask-api .
```

Once the image is built and tagged, you can run the image by mounting local volume to container's WORK_DIR. gunicorn is configured to reload on file change. 

So this basically provides dockerised dev env, where you can code and at the same time it reflects the changes on docker. To run the tagged image:

```
$ docker run --rm -p 5000:5000 -v $(pwd):/usr/src/app flask-api
```

A template of docker-compose.yml file is also provided to make the development process hassle free. It starts up all the project dependencies at once. It also restarts the api server on failuer, so that while development in case due to syntax error container fails to restart, docker-compose keeps on retrying to start the container. Behaviour can be changed by modifying the docker-compose.yml file. To run the docker-compose:

```
$ docker-compose up
```