
import time
import logging
import struct
import random
import types

log = logging.getLogger('probepoint')
hdlr = logging.FileHandler('probepoint.txt')
formatter = logging.Formatter('%(asctime)s %(message)s')
hdlr.setFormatter(formatter)
log.addHandler(hdlr)
log.setLevel(logging.DEBUG)

probepoints = [
    'PROBEPOINT_'
]

class Logger():

    def __init__(self, node_id):
        self.node_id = node_id

    def info(self, probepointname, tracestr):
        if probepointname in probepoints:
            log.debug('{} {} {}'.format(self.node_id, probepointname, tracestr))
        else:
            print('discard info message of unkown probepoint')
