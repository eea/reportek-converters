from StringIO import StringIO
import json
from fabric.api import *
from fabric.contrib.files import exists
from fabric.contrib.project import upload_project
from path import path


env['sarge_home'] = path('/var/local/cdr-converters')
env['converters_venv'] = env['sarge_home'] / 'var' / 'converters-venv'
env['python_bin'] = '/usr/local/Python-2.7.3/bin/python'

project_dir = path(__file__).parent


CONVERT_SCRIPT = """\
#!/bin/sh
exec {converters_venv}/bin/python {instance_dir}/convert.py "$@"
"""


RUN_TESTS_SCRIPT = """\
#!/bin/sh
exec {converters_venv}/bin/python {instance_dir}/run_tests.py "$@"
"""


def sarge(cmd):
    return run("{sarge_home}/bin/sarge {cmd}".format(cmd=cmd, **env))


def quote_json(config):
    return "'" + json.dumps(config).replace("'", "\\u0027") + "'"


@task
def virtualenv():
    if not exists(env['converters_venv']):
        run("virtualenv '{converters_venv}' -p '{python_bin}'"
            " --distribute --no-site-packages"
            .format(**env))

    put("requirements.txt", str(env['converters_venv']))
    run("{converters_venv}/bin/pip install"
        " -r {converters_venv}/requirements.txt"
        .format(**env))


@task
def install(instance_id):
    instance_dir = env['sarge_home'] / instance_id
    upload_project(str(project_dir / 'tests'), str(instance_dir))
    put(str(project_dir / 'convert.py'), str(instance_dir))
    put(str(project_dir / 'run_tests.py'), str(instance_dir))
    put(StringIO(CONVERT_SCRIPT.format(instance_dir=instance_dir, **env)),
        str(env['sarge_home'] / 'bin' / 'convert'),
        mode=0755)
    put(StringIO(RUN_TESTS_SCRIPT.format(instance_dir=instance_dir, **env)),
        str(env['sarge_home'] / 'bin' / 'run_tests'),
        mode=0755)


@task
def clean_old(name):
    for instance in json.loads(sarge('list'))['instances']:
        if instance['meta']['APPLICATION_NAME'] != name:
            continue
        sarge("stop " + instance['id'])
        sarge("destroy " + instance['id'])


@task
def deploy(name='converters'):
    execute('clean_old', name)
    instance_config = {'application_name': name}
    instance_id = sarge("new " + quote_json(instance_config))
    execute('install', instance_id)
