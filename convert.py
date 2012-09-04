#!/usr/bin/env python
import subprocess


def call(converter, filename):
    if converter == 'list_7zip':
        return subprocess.check_output(['7za', 'l', filename])
    elif converter == 'rar2list':
        return subprocess.check_output(['unrar', 'l', filename])
    else:
        raise NotImplementedError
