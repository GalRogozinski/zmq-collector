import zmq
import re

context = zmq.Context()

def subscribe_socket(url):
    socket1 = context.socket(zmq.SUB)
    socket1.setsockopt(zmq.SUBSCRIBE, b'ast')
    socket1.setsockopt(zmq.SUBSCRIBE, b'cs')
    socket1.setsockopt(zmq.SUBSCRIBE, b'qss')
    socket1.connect(url)
    poller1 = zmq.Poller()
    poller1.register(socket1)
    search = re.search('tcp://(.*).devnet.iota.cafe:5556', url)
    return [socket1, poller1, search.group(1)]


sub_list = []

# sub_list.append(subscribe_socket("tcp://iri01.devnet.iota.cafe:5556"))
sub_list.append(subscribe_socket("tcp://iri02.devnet.iota.cafe:5556"))
sub_list.append(subscribe_socket("tcp://bare01.devnet.iota.cafe:5556"))
sub_list.append(subscribe_socket("tcp://bare02.devnet.iota.cafe:5556"))
sub_list.append(subscribe_socket("tcp://bare03.devnet.iota.cafe:5556"))
sub_list.append(subscribe_socket("tcp://alt01.devnet.iota.cafe:5556"))
sub_list.append(subscribe_socket("tcp://alt02.devnet.iota.cafe:5556"))


while True:
    for triplet in sub_list:
        socket, poller, name = triplet
        socks = dict(poller.poll())
        if socket in socks and socks[socket] == zmq.POLLIN:
            message = socket.recv()
            print(name + ': ' + str(message))




