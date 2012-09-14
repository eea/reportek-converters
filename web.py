#!/usr/bin/env python
import flask
import flask.ext.script
import tempfile

from convert import call

web = flask.Blueprint("web", __name__)


def create_app():
    app = flask.Flask(__name__)
    app.register_blueprint(web)
    return app


@web.route("/")
def home():
    return 'Reportek converters'


@web.route("/convert/<string:name>", methods=["POST"])
def convert(name):
    document = flask.request.files.get('file', '')
    with tempfile.NamedTemporaryFile() as tmp:
        pos = 0
        size = 10
        chunk = document.stream.read(size)
        while chunk:
            tmp.file.write(chunk)
            pos+=size
            tmp.seek(pos)
            chunk = document.stream.read(size)
        tmp.file.flush()
        tmp.file.seek(0)
        try:
            response = call(name, tmp.name)
        except:
            #TODO return error response
            raise NotImplementedError
        else:
            return flask.Response(response, direct_passthrough=True, content_type="application/octet-stream")


manager = flask.ext.script.Manager(create_app())
if __name__ == "__main__":
    manager.run()

