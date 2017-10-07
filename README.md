P_MUL - A Reliable Multicast Transfer Protocol
==============================================

P_MUL is an application protocol based on UDP/IP which implements the reliable transfer
of bulk data over a multicast capable IP network. It is based on the IETF draft specification 
described in https://tools.ietf.org/html/draft-riechmann-multicast-mail-00. 

Usage
-----

```python
import pmul
import asyncio

local_ipaddr = '127.0.0.1'
mcast_ipaddr = '225.0.0.1'
mcast_ttl = 1
data_port = 2740
ack_port = 2741

loop = asyncio.get_event_loop()
pmul = pmul.Pmul(local_ipaddr, mcast_ipaddr, mcast_ttl, data_port, ack_port, loop=loop)
loop.run_until_complete(pmul.sendto("abcd".encode("ascii"), ["198.18.10.1"]))
loop.close()
```

Further examples can be found in the examples/ directory.

Feature-Set
-----------

This implementation includes the following improvements compared to the original specification:

- Window-based Congestion Control

- Dynamic Adaptation of Protocol Timers

  ​

### Window-based Congestion Control

Originally P_MUL was designed to operate in broadcast networks with static transmission rates. 
In modern multhop MANET networks the available bandwidth is changing often. Thus a communication protocol must be able to adapt its sending rate to the current available bandwitdh.

To support such modern networks P_MUL was extended to support a simple method to adapt its sending rate to the available bandwidth. In detail the receiver of a message reports the air datarate to the sender 
using the ACK-PDU. The sender then can change its sending rate based on the reported Air datarates of all receivers.

This method has some drawbacks. Since the sender gets the information about the air datarate not until
it had sent all fragments of the message it can react to changing channel conditions very late.
This often results packet loss due to buffer overflow. To improve this mechanism a window based 
transmission method similar to TCP is implemented. 

In general a message of bulk data is fragmented into a list of smaller MTU-sized fragments. 
Normally P_MUL would send all fragments in a continuous transmission phase waiting for the 
ACK-PDUs of all receivers. In the improved version the sender will not send all fragments
at once but only a small window of fragments allowing the receivers to respond with ACK-PDUs
more early. After sending a window of fragments the size of the window is dynamically
adjusted based on the channel quality.

### Dynamic Adapation of Protocol timers

There are two important protocol timers which influences the performance of the message transfer.
* Retransmission timer
* Last PDU Timer

The Retransmission timer is used by the sender to trigger the retransmission of un-acked Data PDUs.
If this timer is calculated too small unneccessary Data PDUs will be sent. If it is too high
the sender will wait too long to retransmit unreceived Data-PDUs. To optimize the performance
the Retransmission timer is calculated dynamically based on the transmission window size and
the current available air datarate.

The Last PDU timer triggers the sending of an ACK-PDU at the receiver of a message. This timer
is also adjusted dynamically based on the current air datarate and the remaining fragments of
the transmission window.

TODOs
-----
* Dynamic adjustment of fragment size based on channel conditions
* Expiration timer for garbage collection
* FEC to improve robustness
