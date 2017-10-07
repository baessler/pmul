#!/usr/bin/python3

import sys
sys.path.append("../")
sys.path.append("../subprojects/")
import airchannel as chan
from pmul import Pmul
from pmul import Observer
import asyncio

class Executor(Observer):
    def __init__(self, loop):
        self.loop = loop
        self.future = None

    def message_received(self, message, from_addr):
        print('CLI: received message of len {} from {}'.format(len(message), from_addr))

    def transmission_finished(self, msid, delivery_status, ack_status):
        print('CLI: transmission of msid: {} finished with {} {}'.format(msid, delivery_status, ack_status))
        self.future.set_result(True)

    async def send_message(self, pmul, dst_addresses, len):
        await asyncio.sleep(3)
        message = 'a';
        for i in range(0,len):
            message += 'a'.format(len);
        bulk_data = message.encode("ascii")
        msid = await pmul.sendto_async(bulk_data, dst_addresses)
        print('sent message with msid: {}'.format(msid))

    def run(self):
        # Channel emulation
        self.channel = chan.WirelessChannel(self.loop)
        self.channel.add_link("198.18.10.250", 50000, 10, 20)
        self.channel.add_link("198.18.20.250", 50000, 10, 20)
        self.channel.add_link("198.18.30.250", 50000, 10, 20)

        # Create the P_MUL instances
        self.pmul1 = Pmul("198.18.10.250", "224.0.1.240", 1, 2740, 2741, loop=self.loop, chan_cli_port=8000, chan_srv_port=8001)
        self.pmul2 = Pmul("198.18.20.250", "224.0.1.240", 1, 2740, 2741, loop=self.loop, chan_cli_port=8002, chan_srv_port=8003)
        self.pmul3 = Pmul("198.18.30.250", "224.0.1.240", 1, 2740, 2741, loop=self.loop, chan_cli_port=8004, chan_srv_port=8005)

        # Register observer at P_MUL protocol
        self.pmul1.set_observer(self)
        self.pmul2.set_observer(self)
        self.pmul3.set_observer(self)

        # send a message of 50kB
        self.future = asyncio.Future()
        asyncio.ensure_future(self.send_message(self.pmul1, ['198.18.20.250','198.18.30.250'], 50000))
        self.loop.run_until_complete(self.future)

async def forever():
    while True:
        try:
            await asyncio.sleep(1)
        except KeyboardInterrupt:
            pass

loop = asyncio.get_event_loop()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    executor = Executor(loop)
    executor.run()
    print('now run until forever')
    loop.run_until_complete(forever())
    loop.close()

