# -*-*- encoding: utf-8 -*-*-

import sys
import json

from flask import request, Blueprint
from flask.ext.wtf import TextField, PasswordField, Required, URL, ValidationError

from labmanager.forms import AddForm, RetrospectiveForm, GenericPermissionForm
from labmanager.rlms import register, Laboratory, BaseRLMS, BaseFormCreator, register_blueprint, Capabilities, Versions
from labmanager import app



class HTTPAddForm(AddForm):

    remote_login = TextField("Login",        validators = [Required()])
    password     = PasswordField("Password")

    base_url     = TextField("Base URL",    validators = [Required(), URL() ])

    def __init__(self, add_or_edit, *args, **kwargs):
        super(HTTPAddAddForm, self).__init__(*args, **kwargs)
        self.add_or_edit = add_or_edit

    @staticmethod
    def process_configuration(old_configuration, new_configuration):
        old_configuration_dict = json.loads(old_configuration)
        new_configuration_dict = json.loads(new_configuration)
        if new_configuration_dict.get('password', '') == '':
            new_configuration_dict['password'] = old_configuration_dict.get('password','')
        return json.dumps(new_configuration_dict)

    def validate_password(form, field):
        if form.add_or_edit and field.data == '':
            raise ValidationError("This field is required.")

    def validate_mappings(form, field):
        try:
            content = json.loads(field.data)
        except:
            raise ValidationError("Invalid json content")
        
        if not isinstance(content, dict):
            raise ValidationError("Dictionary expected")
        
        for key in content:
            if not isinstance(key, basestring):
                raise ValidationError("Keys must be strings")
           
            if '@' not in key:
                raise ValidationError("Key format: experiment_name@experiment_category ")
                
            value = content[key]
            if not isinstance(value, basestring):
                raise ValidationError("Values must be strings")
           
            if '@' not in value:
                raise ValidationError("Value format: experiment_name@experiment_category ")

class HTTPPermissionForm(RetrospectiveForm):
    priority = TextField("Priority")
    time     = TextField("Time (in seconds)")

    def validate_number(form, field):
        if field.data != '' and field.data is not None:
            try:
                int(field.data)
            except:
                raise ValidationError("Invalid value. Must be an integer.")


    validate_priority = validate_number
    validate_time     = validate_number

class HTTPLmsPermissionForm(HTTPPermissionForm, GenericPermissionForm):
    pass

class HTTPFormCreator(BaseFormCreator):

    def get_add_form(self):
        return HTTPAddForm

    def get_permission_form(self):
        return HTTPPermissionForm

    def get_lms_permission_form(self):
        return HTTPLmsPermissionForm

FORM_CREATOR = HTTPFormCreator()



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
