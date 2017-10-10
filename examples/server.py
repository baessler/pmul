#!/usr/bin/python3

import sys
sys.path.append("../")
import pmul
import asyncio

class ServerProtocol(pmul.PmulProtocol):
    def __init__(self, conf):
        self.__conf = conf

    def connection_made(self, transport):
        self.transport = transport
        print('P_MUL protocol is ready')
        
    def data_received(self, data, addr):
        print("Received data from {}".format(addr))

    def delivery_completed(self, msid, delivery_status, ack_status):
        print('Delivery of Message-ID {} finished with {} {}'.format(msid, delivery_status, ack_status))

async def forever():
    while True:
        try:
            await asyncio.sleep(1)
        except KeyboardInterrupt:
            pass

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    conf = pmul.conf_init()
    coro = pmul.create_pmul_endpoint(ServerProtocol, loop, conf);
    protocol, transport = loop.run_until_complete(coro)
    loop.run_until_complete(forever())
    loop.close()

