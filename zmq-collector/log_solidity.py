import zmq
import re
import plotly.graph_objects as go

context = zmq.Context()

names = []
sub_list = []


def create_plot():
    columns = ['Transactions'] + names
    table = go.Figure(data=[go.Table(header=dict(values=columns),
                                   cells=dict(values=[[]]*len(columns)))
                          ])
    return table

def update_plot(name, tx, is_solid):
    table = fig.data[0]
    table_data = table.cells.values
    column_index = names.index(name) + 1
    if tx in table_data[0]:
        row_index = table.cells.values[0].index(tx)
        table.cells.values[column_index].insert(row_index, is_solid)
        all_true = table.cells.values[column_index].count(True) == len(names)
        if all_true:
            [elem.pop(row_index) for elem in table.cells.values]
    else:
        table_data = list(table_data)
        table_data[0].append(tx)
        row_index = table_data[0].index(tx)
        print(table_data)
        print(column_index)
        print(row_index)
        table_data[column_index].insert(row_index, is_solid)
        table.cells.values = table_data




def subscribe_socket(url):
    socket1 = context.socket(zmq.SUB)
    # socket1.setsockopt(zmq.SUBSCRIBE, b'ast')
    # socket1.setsockopt(zmq.SUBSCRIBE, b'cs')
    socket1.setsockopt(zmq.SUBSCRIBE, b'qss')
    socket1.connect(url)
    poller1 = zmq.Poller()
    poller1.register(socket1)
    machine_name = re.search('tcp://(.*).devnet.iota.cafe:5556', url).group(1)
    names.append(machine_name)
    return [socket1, poller1, machine_name]



# sub_list.append(subscribe_socket("tcp://iri01.devnet.iota.cafe:5556"))
sub_list.append(subscribe_socket("tcp://iri02.devnet.iota.cafe:5556"))
sub_list.append(subscribe_socket("tcp://bare01.devnet.iota.cafe:5556"))
sub_list.append(subscribe_socket("tcp://bare02.devnet.iota.cafe:5556"))
sub_list.append(subscribe_socket("tcp://bare03.devnet.iota.cafe:5556"))
sub_list.append(subscribe_socket("tcp://alt01.devnet.iota.cafe:5556"))
sub_list.append(subscribe_socket("tcp://alt02.devnet.iota.cafe:5556"))

fig = create_plot()
fig.show()

while True:
    for triplet in sub_list:
        socket, poller, name = triplet
        socks = dict(poller.poll())
        if socket in socks and socks[socket] == zmq.POLLIN:
            message = socket.recv()
            message_split = str(message).split(" ")
            tx = message_split[1]
            is_solid = bool(message_split[2])
            update_plot(name, tx, is_solid)
            print(name + ': ' + str(message))




