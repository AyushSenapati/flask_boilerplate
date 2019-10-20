import os
from jinja2 import Template


APP_ROOT = 'app'
SERVICE_DIR = 'services'

while True:
    service_name = 'service_' + input('Service Name: ')
    print(f"About to create a service with name: {service_name}")
    input_ = input("Confirm? (y/N): ")
    if input_.lower() == 'y':
        break

# Create SERVICE_DIR if not exists in APP_ROOT dir
if not os.path.exists(SERVICE_DIR):
    os.mkdir(SERVICE_DIR)

# Create a service dir inside SERVICE_DIR
os.mkdir(f"{SERVICE_DIR}/" + service_name)

## Populate the new service with necessary files/dirs
# DIRs to be created for a service
dirs = ['controllers', 'models', 'tests', 'custom_exceptions']
for dir_ in dirs:
    path = os.path.join(SERVICE_DIR, service_name, dir_)
    os.mkdir(path)
    print(f"\t{path}/ created.")

## Populate the files with appropriate content
urls_file_template = '''
from flask import Blueprint
from flask_restful import Api

# Import controllers to create routes

# Class to handle service specific global exception
class ExtendedAPI(Api):
    def handle_error(self, err):
        pass

{{service_name}}_bp = Blueprint('{{service_name}}', __name__)
{{service_name}}_api = ExtendedAPI({{service_name}}_bp)

# Service specific routes goes here
# EX: {{service_name}}_api.add_resource(ControllerName, '/route')

'''
url_tm = Template(urls_file_template)
rendered_url_tm = url_tm.render(service_name=service_name)

# Create appropriate files with service specific content
fnames = {'__init__': '', 'urls': rendered_url_tm}
for fname in fnames:
    path = os.path.join(SERVICE_DIR, service_name, fname + '.py')
    with open(path, "w") as fo:
        fo.write(fnames[fname])
    print(f"\t{path} created")

print(f"NOTE: Add the service: '{service_name}' to the " \
    "INSTALLED_SERVICES in the settings file")