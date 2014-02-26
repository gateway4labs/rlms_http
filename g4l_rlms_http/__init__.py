# -*-*- encoding: utf-8 -*-*-

import sys
import json

from flask import request, Blueprint
from flask.ext.wtf import TextField, PasswordField, Required, URL, ValidationError

from labmanager.forms import AddForm, RetrospectiveForm, GenericPermissionForm
from labmanager.rlms import register, Laboratory, BaseRLMS, BaseFormCreator, register_blueprint, Capabilities, Versions
from labmanager import app

class RLMS(BaseRLMS):
    def __init__(self, configuration):
        self.configuration = json.loads(configuration)
        self.http_url = self.configuration['url']
        self.http_user = self.configuration['user']
        self.http_passwd = self.configuration['passwd']
        self.http_config = self.configuration['config'] # String, que es un JSON

    def get_module(version):
        """get_module(version) -> proper module for that version

        Right now, a single version is supported, so this module itself will be returned.
        When compatibility is required, we may change this and import different modules.
        """
        # TODO: check version
        return sys.modules[__name__]


    def get_version(self):
         
        return Versions.VERSION_1

    def get_capabilities(self):
        
        return Versions.VERSION_1

    def test(self):
         
        return None

    def get_laboratories(self):

        return None
        
    def reserve(self, laboratory_id, username, institution, general_configuration_str, particular_configurations, request_payload, user_properties, *args, **kwargs):
        return None




http_blueprint = Blueprint('http', __name__)
@http_blueprint.route('/')
def index():
    return "This is the index for HTTP"

register("HTTP", ['0.1'], __name__)
register_blueprint(http_blueprint, '/http')
