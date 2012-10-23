import logging
import sys
from logging import StreamHandler

conversion_log = logging.getLogger('convert.monitoring')

def initialize():
    conversion_log.addHandler(StreamHandler(stream=sys.stderr))
