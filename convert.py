#!/usr/bin/env python
import flask
import subprocess
from utils import mime_type


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
        self.__compatibility__init__(title, ct_schema, ct_extraparams, description, ct_suffix)


    def __compatibility__init__(self, title, ct_schema, ct_extraparams, description, ct_suffix):
        """used for compatibility"""
        #TODO refactor Reportek and eliminate this function

        self.title = title or self.name
        self.description = description
        if self.accepted_content_types:
            self.ct_input = self.accepted_content_types[0]
        else:
            self.ct_input = ''
        self.ct_output = self.returned_content_type
        self.ct_schema = ''
        self.ct_extraparams = []
        self.suffix = ''



converters = {'list_7zip': Converter('list_7zip', '7za l %s', mime_type('7z')),
              'rar2list': Converter('rar2list', 'unrar l %s', mime_type('rar'), title='List of contents')}


def list_converters():
    return converters.keys()


def list_converters_params():
    results = []
    app = flask.current_app
    for conv in converters.values():
        name = '{prefix}{name}'.format(prefix=app.config.get('PREFIX', ''),
                                       name = conv.name)
        results.append(
            [name, #id
             conv.title, #title
             '/convert/%s' %conv.name, #convert_url
             conv.ct_input, #ct_input
             conv.ct_output, #ct_output
             conv.ct_schema, #ct_schema
             conv.ct_extraparams, #ct_extraparams
             conv.description, #description
             conv.suffix] #suffix
        )
    return results

def call(converter_id, filename):
    converter = converters.get(converter_id, None)
    if converter:
        command = converter.command
        return subprocess.check_output(command %filename, shell=True)
    else:
        raise NotImplementedError
