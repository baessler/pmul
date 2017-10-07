#!/usr/bin/python3

"""
This script creates a P_MUL client which delivers multiple messages to a destination P_MUL server.
"""

import sys
sys.path.append("../")
import pmul
import asyncio
import argparse

class Client(pmul.Observer):
    def __init__(self, loop):
        self.loop = loop

    def message_received(self, message, from_addr):
        print('CLI: received message of len {} from {}'.format(len(message), from_addr))

    def transmission_finished(self, msid, delivery_status, ack_status):
        print('CLI: transmission of msid: {} finished with {} {}'.format(msid, delivery_status, ack_status))

    async def send_message(self, dst_address, len):
        await asyncio.sleep(3)
        message = 'a';
        for i in range(0,len):
            message += 'a'.format(len);
        bulk_data = message.encode("ascii")
        result = await self.pmul.sendto(bulk_data, [dst_address])
        print('CLI: delivery finished with {} {}'.format(result[0], result[1]))

    async def run(self, conf):
        self.pmul = pmul.Pmul(conf['local_addr'], conf['mcast_addr'], 1, 2740, 2741, loop=self.loop)
        self.pmul.set_observer(self)

        for i in range(0,conf['num']):
            print('send message {} of len {} to {}'.format(i, conf['message_len'], conf['destination']))
            await self.send_message(conf['destination'], conf['message_len'])

        print('finished message transmission')

async def forever():
    while True:
        try:
            await asyncio.sleep(1)
        except KeyboardInterrupt:
            pass

def init_arguments(conf):
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--bind', type=str)
    parser.add_argument('-d', '--destination', type=str)
    parser.add_argument('-m', '--multicast', type=str)
    parser.add_argument('-l', '--length', type=int)
    parser.add_argument('-n', '--num', type=int)
    args = parser.parse_args()

    conf['local_addr'] = '127.0.0.1'
    if args.bind is not None:
        conf['local_addr'] = '127.0.0.1'

    conf['destination'] = '127.0.0.1'
    if args.destination is None:
        parser.print_help()
        exit()

    conf['mcast_addr'] = '225.0.0.1'
    if args.multicast is not None:
        conf['mcast_addr'] = args.multicast

    conf['message_len'] = 5000
    if args.length is not None:
        conf['message_len'] = args.length

    conf['num'] = 10
    if args.num is not None:
        conf['num'] = args.num


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    conf = dict()
    init_arguments(conf)
    
    print('client: {}'.format(conf))

    srv = Client(loop)
    asyncio.ensure_future(srv.run(conf))
    loop.run_until_complete(forever())
    loop.close()

