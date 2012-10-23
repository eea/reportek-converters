import logging
import sys
from logging import StreamHandler

logging.basicConfig(format='%(asctime)s [%(levelname)s]: %(message)s',
                    datefmt='%d/%m/%Y %I:%M:%S %p')
conversion_log = logging.getLogger('web.conversion')

def initialize():
    conversion_log.addHandler(StreamHandler(stream=sys.stderr))
