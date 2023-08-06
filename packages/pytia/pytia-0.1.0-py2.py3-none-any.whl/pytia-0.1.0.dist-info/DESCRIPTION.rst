# pytia

pytia is a basic Python implementation of a TOBI interface A (TiA) server. TiA is a data transmission protocol developed as part of the [TOBI project](http://www.tobi-project.org). It is designed to allow a server acquiring data from multiple sensors to stream that data efficiently to one or more clients over TCP or UDP. For more information see [here](http://tools4bci.sourceforge.net/tia.html) and [here](http://tools4bci.sourceforge.net/signalserver.html).

# Basic example

The bulk of the code in pytia implements a TiA server, but it also contains a 
usable client class for testing or basic streaming. A minimal example of a TiA
client/server setup would look like this:

## Server

Create a server listening on a local port:
```python
from pytia import TiAServer, TiAConnectionHandler, TiASignalConfig
server = TiAServer(('', 9000), TiAConnectionHandler)
```
Before starting the server, you must define at least 1 "signal", a source of data
that the server can poll and stream to clients. Signals are defined using a 
list of TiASignalConfig objects:
```python
def sig_callback(id):
    return [random.uniform(-10, 10) for x in range(3)]
# create a 50Hz, 3 channel signal with 1 sample per channel per packet.
# "signal_callback" is a callable the server will call to retrieve data for
# this signal. You shouldn't do long-running work in it! 
server.start([TiASignalConfig(channels=3, sample_rate=50, blocksize=1, callback=sig_callback, id=0, is_master=True, sigtype=TIA_SIG_USER_1)])
```

## Client

Now the server is running, a client can connect to it as follows:
```python
from pytia import TiAClient

server_address = '127.0.0.1'
client = TiAClient(server_address, 9000)
if not client.connect():
    # handle error

# TiA clients should start by checking the server protocol version matches their own...
if not client.cmd_check_protocol_version():
    client.disconnect()
    # handle error

# to begin streaming data, a client should request a data connection from the
# server. The server will send back a port number and the client then connects
# to that port to obtain the connection. 
status, dport = client.cmd_get_data_connection_tcp()
if not status:
    client.disconnect()
    # handle error

if not client.start_streaming_data_tcp(server_address, dport):
    client.disconnect()
    # handle error

# now we can retrieve the data being streamed from the server
# the get_data method returns a list of packets. The number of packets can 
# vary from call to call depending on when you call it and the number of
# signals the server is sending. 
packets = client.get_data()

# each packet is an instance of TiAPacket. It contains:
#   - packet.signals (a list of the data for each signal in the packet)
#   - packet.blocksizes (a list of the block sizes for each signal)
#   - packet.channels (a list of the number of channels in each signal)
#   - packet.packet_number (sequence number)
#   - packet.timestamp (timestamp set on transmission)
#   - packet.packet_id (currently set to the same as sequence number)

# example of extracting some data from a packet
if len(packets) > 0:
    packet = packets[0]

    print('Packet contains %d signals' % (len(packet.signals)))
    print('Number/timestamp/ID: ', packet.packet_number, packet.timestamp, packet.packet_id)
    print('Channel counts: ', packet.channels)

    # access some data by channel
    data = packet.get_channel(0, 1) # channel 1 from signal 0   
    print('Signal 0/channel 1 = ', data)

    # or just get all the data from a selected signal
    data = packet.get_channel(0)
    print('Signal 0 = ', data)


# disconnect from the server when done streaming
client.stop_streaming_data()
client.disconnect()
```


