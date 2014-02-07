#!/usr/bin/env python
import flask
import json
import subprocess
import tempfile
import path
import os
from path import path
import logging

logging.basicConfig(format='%(asctime)s [%(levelname)s]: %(message)s',
                    datefmt='%d/%m/%Y %I:%M:%S %p')
conversion_log = logging.getLogger(__name__ + '.monitoring')
conversion_log.setLevel(logging.DEBUG)

class ConversionError(Exception):
    """ Raised when returncode is not 0  """


def init_converters():
    config_path = path(__file__).parent.abspath() / 'config'
    params = json.loads((config_path / 'converters.json').bytes())
    return {args.pop('name'): Converter(**args)
            for args in params}


def call(converter_id, filename, extra_args=[]):
    format_params = [filename] + extra_args
    converter = converters.get(converter_id, None)
    if converter:
        command = converter.command
        tmp_dir = tempfile.mkdtemp(prefix="tmp")
        try:
            response = subprocess.check_output(
                           command.format(*format_params),
                           stderr=subprocess.STDOUT,
                           cwd=tmp_dir,
                           env=dict(os.environ,
                                    SCRIPTS=path(os.getcwd()) / 'bin',
                                    LIB=path(os.getcwd()) / 'lib',
                                    TMPDIR = tmp_dir,
                                    TEMP = tmp_dir,
                                    TMP = tmp_dir),
                           shell=True)
            return response
        except subprocess.CalledProcessError as exp:
            cexp = ConversionError()
            cexp.output = exp.output
            message = ('[CONVERSION ERROR]\n'
                       'converter id: %s\n'
                       'output: %s')
            try:
                exp.output.decode('ascii')
            except UnicodeDecodeError:
                conversion_log.warning(message %(converter_id,
                                                 '[unable to display]\n')
                                      )
            else:
                conversion_log.warning(message %(converter_id, exp.output))
            raise cexp
        finally:
            path(tmp_dir).rmtree()
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
        tag = app.config.get('TAG', '')
        if tag:
            title = '{title} {tag}'.format(title=conv.title,
                                           tag='(%s)' %tag)
        else:
            title = '{title}'.format(title=conv.title)
        results.append(
            [name, #id
             title, #title
             'convert/%s' %(conv.name), #convert_url
             conv.ct_input, #ct_input
             conv.ct_output, #ct_output
             conv.ct_schema, #ct_schema
             conv.extraparams, #ct_extraparams
             conv.description] #description
        )
    return results


class Converter(object):

    def __init__(self, name, command, accepted_content_types,
                returned_content_type='text/plain;charset="utf-8"',
                title='',
                extraparams=[],
                description = '',
                ct_schema='',
                additional_files=None):
        self.name = name
        self.command = command
        self.accepted_content_types = accepted_content_types #lista
        self.returned_content_type = returned_content_type
        self.extraparams = extraparams
        self.additional_files = additional_files
        self.__compatibility__init__(title,
                                     ct_schema,
                                     description)


    def __compatibility__init__(self, title, ct_schema, description):
        """used for compatibility"""
        #TODO refactor Reportek and eliminate this function

        self.title = title or self.name
        self.description = description
        if self.accepted_content_types:
            self.ct_input = self.accepted_content_types
        else:
            self.ct_input = ''
        self.ct_output = self.returned_content_type
        self.ct_schema = ct_schema


converters = init_converters()
