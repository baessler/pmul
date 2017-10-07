#!/usr/bin/python3

"""
This script creates a P_MUL client which delivers multiple messages to a destination P_MUL server.
"""

import sys
sys.path.append("../")
import pmul
import asyncio

local_ipaddr = '127.0.0.1'
mcast_ipaddr = '225.0.0.1'
mcast_ttl = 1
data_port = 2740
ack_port = 2741

loop = asyncio.get_event_loop()
pmul = pmul.Pmul(local_ipaddr, mcast_ipaddr, mcast_ttl, data_port, ack_port, loop=loop)
loop.run_until_complete(pmul.sendto("abcd".encode("ascii"), ["127.0.0.1"]))
loop.close()