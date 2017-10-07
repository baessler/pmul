#!/usr/bin/python3

import sys
sys.path.append("../")
sys.path.append("../subprojects/")
from pmul import Pmul
from pmul import Observer
import asyncio

class Server(Observer):
    def __init__(self, loop):
        self.loop = loop

    def message_received(self, message, from_addr):
        print('CLI: received message of len {} from {}'.format(len(message), from_addr))

    def transmission_finished(self, msid, delivery_status, ack_status):
        print('CLI: transmission of msid: {} finished with {} {}'.format(msid, delivery_status, ack_status))

    def run(self):
        self.pmul = Pmul("192.168.2.106", "225.0.0.1", 1, 2740, 2741, loop=self.loop)
        self.pmul.set_observer(self)

async def forever():
    while True:
        try:
            await asyncio.sleep(1)
        except KeyboardInterrupt:
            pass

loop = asyncio.get_event_loop()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    srv = Server(loop)
    srv.run()
    loop.run_until_complete(forever())
    loop.close()

