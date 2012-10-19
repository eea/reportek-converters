#!/usr/bin/env python
import flask
import json
import subprocess
from path import path
from utils import mime_type, extension

class ConversionError(Exception):
    """ Raised when returncode is not 0  """


def init_converters():
    config_path = path(__file__).parent.abspath() / 'config'
    params = json.loads((config_path / 'converters.json').bytes())
    return {conv[0]: Converter(*conv[0:3],
                                title=conv[3],
                                returned_content_type=conv[4])
            for conv in params}


def list_converters():
    return converters.keys()


def list_converters_params():
    results = []
    app = flask.current_app
    for conv in init_converters().values():
        name = '{prefix}{name}'.format(prefix=app.config.get('PREFIX', ''),
                                       name = conv.name)
        title = '{title} {tag}'.format(title=conv.title,
                                       tag='(%s)' %app.config.get('TAG', ''))
        results.append(
            [name, #id
             title, #title
             'convert/%s' %(conv.name), #convert_url
             conv.ct_input, #ct_input
             conv.ct_output, #ct_output
             conv.ct_schema, #ct_schema
             conv.ct_extraparams, #ct_extraparams
             conv.description, #description
             conv.suffix] #suffix
        )
    return results

def call(converter_id, filename, extra_args=[]):
    format_params = [filename] + extra_args
    converter = init_converters().get(converter_id, None)
    if converter:
        command = converter.command
        try:
            response = subprocess.check_output(
                           command.format(*format_params),
                           stderr=subprocess.STDOUT,
                           shell=True)
            return response
        except subprocess.CalledProcessError as exp:
            cexp = ConversionError()
            cexp.output = exp.output
            raise cexp
    else:
        raise NotImplementedError

def list_converters():
    return converters.keys()


def list_converters_params():
    results = []
    app = flask.current_app
    for conv in converters.values():
        name = '{prefix}{name}'.format(prefix=app.config.get('PREFIX', ''),
                                       name = conv.name)
        title = '{title} {tag}'.format(title=conv.title,
                                       tag='(%s)' %app.config.get('TAG', ''))
        results.append(
            [name, #id
             title, #title
             'convert/%s' %(conv.name), #convert_url
             conv.ct_input, #ct_input
             conv.ct_output, #ct_output
             conv.ct_schema, #ct_schema
             conv.ct_extraparams, #ct_extraparams
             conv.description, #description
             conv.suffix] #suffix
        )
    return results


class Converter(object):

    def __init__(self, name, command, accepted_content_types,
                returned_content_type='text/plain;charset="utf-8"',
                title=None,
                ct_schema=None,
                ct_extraparams=None,
                description = '',
                ct_suffix=None):
        self.name = name
        self.command = command
        self.accepted_content_types = accepted_content_types #lista
        self.returned_content_type = returned_content_type
        self.__compatibility__init__(title,
                                     ct_schema,
                                     ct_extraparams,
                                     description,
                                     ct_suffix)


    def __compatibility__init__(self, title, ct_schema, ct_extraparams, description, ct_suffix):
        """used for compatibility"""
        #TODO refactor Reportek and eliminate this function

        self.title = title or self.name
        self.description = description
        if self.accepted_content_types:
            self.ct_input = self.accepted_content_types
        else:
            self.ct_input = ''
        self.ct_output = self.returned_content_type
        self.ct_schema = ''
        self.ct_extraparams = []
        for mime in self.accepted_content_types:
            ext = extension(mime)
            if ext:
                break
        else:
            ext = ''
        self.suffix = ext


converters = init_converters()
