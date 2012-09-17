#!/usr/bin/env python
import subprocess

converters = {'list_7zip': ['7za', 'l'],
              'rar2list': ['unrar', 'l'],
             }

def list_converters(self):
    return converters.keys()

def call(converter_id, filename):
    command = converters.get(converter_id, None)
    if command:
        return subprocess.check_output(command + [filename])
    else:
        raise NotImplementedError
