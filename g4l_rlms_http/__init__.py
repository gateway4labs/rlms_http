# -*-*- encoding: utf-8 -*-*-

import sys
import json

from flask import request, Blueprint
from flask.ext.wtf import TextField, PasswordField, Required, URL, ValidationError

from labmanager.forms import AddForm, RetrospectiveForm, GenericPermissionForm
from labmanager.rlms import register, Laboratory, BaseRLMS, BaseFormCreator, register_blueprint, Capabilities, Versions
from labmanager import app

from .http_client import HTTPClient
from .http_data import ExperimentId


class RLMS(BaseRLMS):
    def __init__(self, configuration):
        self.configuration = json.loads(configuration)
        self.http_url = self.configuration['url']
        self.http_user = self.configuration['user']
        self.http_passwd = self.configuration['passwd']
        self.http_config = self.configuration['config'] # String, que es un JSON


    def get_version(self):
        # Esto es genérico, no hace falta los datos
        return_value = requests.get(self.http_url + "/version")
        if return_value in Versions.LOQUESEA:
             return ...
        return Versions.VERSION_1

    def get_capabilities(self):
        # Esto es genérico, no hace falta los datos
        return_value = requests.get(self.http_url + "/capabilities")
        if return_value in Versions.LOQUESEA:
             return ...
        return Versions.VERSION_1

    def test(self):
        json.loads(self.configuration)
        # TODO
        return None

    def get_laboratories(self):
        # Opción 1:
        plugin_config = json.loads(self.http_config) # { 'sb_guid' : '12345', 'auth_guid' : 'foobar' }
        headers = {}
        for key, value in plugin_config.iteritems(): 
            headers['g4l-%s' % key] = value

        return_value = requests.get(self.http_url + "/laboratories", headers = headers)
        return parsearlo
        # Opción 2:
        return_value = requests.post(self.http_url + "/laboratories", data = self.http_config)

    def reserve(self, laboratory_id, username, institution, general_configuration_str, particular_configurations, request_payload, user_properties, *args, **kwargs):
        data = { 
                  'reservation_data' : {
                   'laboratory_id'  : laboratory_id ... 
                  },
                  'plugin_data' : json.loads(self.http_config)
               }
                   
        requests.post(self.http_url + '/laboratories/<laboratory_id>/reserve', data = data)





http_blueprint = Blueprint('http', __name__)
@http_blueprint.route('/')
def index():
    return "This is the index for HTTP"

register("HTTP", '5.0', __name__)
register_blueprint(http_blueprint, '/http')
