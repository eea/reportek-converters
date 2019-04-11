#!/usr/bin/env python
import flask
from flask_script import Manager
import tempfile
import base64
import logging
import os
import time

from convert import (call, list_converters,
                     list_converters_params, converters,
                     ConversionError)

logging.basicConfig(format='%(asctime)s [%(levelname)s]: %(message)s',
                    datefmt='%d/%m/%Y %I:%M:%S %p', level=logging.DEBUG)
logger = logging.getLogger(__name__ + '.monitoring')
logger.setLevel(logging.DEBUG)

web = flask.Blueprint("web", __name__)


def create_app():
    app = flask.Flask(__name__)
    app.config.from_pyfile("settings.py", silent=True)
    app.register_blueprint(web)
    return app


@web.route("/")
def home():
    return 'Reportek converters'

@web.route("/list")
def available_converters():
    return flask.jsonify({'list': list_converters()})


@web.route("/params")
def converters_params():
    response = {'list': list_converters_params()}
    prefix =  flask.current_app.config.get('PREFIX', None)
    if prefix:
        response.update({'prefix': prefix})
    return flask.jsonify(response)

@web.route("/params/<string:name>", methods=["GET"])
def specific_params(name=None):
    if name in list_converters():
        converter = converters.get(name)
        output = {
            'id': converter.name,
            'title': converter.title,
            'convert_url': 'convert/%s' %(converter.name),
            'ct_input': converter.ct_input,
            'ct_output': converter.ct_output,
            'ct_schema': converter.ct_schema,
            'ct_extraparams': converter.extraparams,
            'description': converter.description,
            'suffix': ''
        }
        return flask.jsonify(output)

@web.route("/convert/<string:name>", methods=["POST"])
def convert(name):
    start = time.time()
    document = getattr(flask.request.files.get('file', ''), 'stream', None)
    if not document:
        import StringIO
        document = StringIO.StringIO(flask.request.data)
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        chunk = True
        while chunk:
            chunk = document.read(10)
            tmp.file.write(chunk)
        tmp.file.flush()
        tmp.file.seek(0)
        file_size = os.path.getsize(tmp.name)
        extra_params = flask.request.form.values()
        if not extra_params:
            extra_params = flask.request.args.values()
        needs_additional_files = getattr(converters.get(name), 'additional_files', False)
        try:
            if needs_additional_files:
                filepath = '.'.join([tmp.name, 'shp'])
                os.link(tmp.name, filepath)
                shx_doc = getattr(flask.request.files.get('shx'), 'stream', None)
                dbf_doc = getattr(flask.request.files.get('dbf'), 'stream', None)
                shx_filepath = '.'.join([tmp.name, 'shx'])
                dbf_filepath = '.'.join([tmp.name, 'dbf'])
                tmp_shx = open(shx_filepath, 'w')
                tmp_dbf = open(dbf_filepath, 'w')
                tmp_shx.write(shx_doc.read())
                tmp_dbf.write(dbf_doc.read())
                tmp_shx.flush()
                tmp_dbf.flush()
                tmp_shx.seek(0)
                tmp_dbf.seek(0)
                extra_params+=[shx_filepath, dbf_filepath]
                response = call(name, filepath, list(extra_params))
                tmp_shx.close()
                tmp_dbf.close()
                os.unlink(filepath)
                os.unlink(shx_filepath)
                os.unlink(dbf_filepath)
            else:
                response = call(name, tmp.name, list(extra_params))
        except ConversionError as exp:
            response = base64.b64encode(exp.output)
            status = 500
            content_type = converters.get(name).ct_output
        except NotImplementedError as exp:
            response = ''
            status = 404
            content_type = 'text/plain'
        else:
            status = 200
            content_type = converters.get(name).ct_output
        finally:
            os.remove(tmp.name)
    duration = time.time() - start
    log_details = {
        'name': name,
        'size': file_size,
        'mime': content_type,
        'duration': duration}
    logger.info(
        ('\nPost conversion details:\n'
        '\tConverter: {name}\n'
        '\tFile size: {size} bytes\n'
        '\tMime-type: {mime}\n'
        '\tDuration:  {duration:.4f} seconds').format(**log_details))
    return flask.Response(response, status=status, content_type=content_type)


app = create_app()
manager = Manager(app)
if __name__ == "__main__":
    manager.run()
