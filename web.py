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
        tmp.file.write(document.stream.next())
        tmp.file.seek(0)
        try:
            response = call(name, tmp.name)
        except:
            #TODO return error response
            raise NotImplementedError
        else:
            return flask.Response(response, content_type="application/octet-stream")


manager = flask.ext.script.Manager(create_app())
if __name__ == "__main__":
    manager.run()

