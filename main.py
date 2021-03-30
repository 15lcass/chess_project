import networkx as nx
import matplotlib.pyplot as plt


class Node:
    def __init__(self, id):
        self.data = id
        self.connections = []


def create_nodes():  # create 64 nodes for the chess board
    nodes = []
    letters = 'abcdefgh'
    for i in range(1, 9):
        for letter in letters:
            new_node = Node('{}{}'.format(letter, i))
            nodes.append(new_node)
    return nodes


def rook_connections(nodes):
    edges = []
    for node1 in nodes:  # wtf is this
        for node2 in nodes:
            if node1.data[0] == node2.data[0] or node1.data[1] == node2.data[1]:
                edges.append((node1.data, node2.data))
                node1.connections.append(node2.data)
                node2.connections.append(node1.data)

    return edges


def king_connections(nodes):
    edges = []
    for node1 in nodes:  # double loop? help
        for node2 in nodes:
            if node1.data[0] == node2.data[0] and int(node1.data[1]) == int(node2.data[1]) + 1:  # checks if 1 square above or below in the same column
                edges.append((node1.data, node2.data))
                node1.connections.append(node2.data)
                node2.connections.append(node1.data)

            elif ord(node1.data[0]) == ord(node2.data[0]) + 1 and node1.data[1] == node2.data[1]:  # checks if 1 square right or left in the same row
                edges.append((node1.data, node2.data))
                node1.connections.append(node2.data)
                node2.connections.append(node1.data)

            elif ord(node1.data[0]) == ord(node2.data[0]) + 1 and int(node1.data[1]) == int(node2.data[1]) + 1:  # diagonal bottom left to top right
                edges.append((node1.data, node2.data))
                node1.connections.append(node2.data)
                node2.connections.append(node1.data)

            elif ord(node1.data[0]) == ord(node2.data[0]) + 1 and int(node1.data[1]) == int(node2.data[1]) - 1:  # diagonal top left to bottom right
                edges.append((node1.data, node2.data))
                node1.connections.append(node2.data)
                node2.connections.append(node1.data)

    return edges


def knight_connections(nodes):
    edges = []
    for node1 in nodes:
        for node2 in nodes:
            if ord(node1.data[0]) == ord(node2.data[0]) + 2 and int(node1.data[1]) == int(node2.data[1]) + 1:  #  left 2, down 1 / right 2, up 1
                edges.append((node1.data, node2.data))
                node1.connections.append(node2.data)
                node2.connections.append(node1.data)

            elif ord(node1.data[0]) == ord(node2.data[0]) + 2 and int(node1.data[1]) == int(node2.data[1]) - 1:  # left 2, up 1 / right 2, down 1
                edges.append((node1.data, node2.data))
                node1.connections.append(node2.data)
                node2.connections.append(node1.data)

            elif ord(node1.data[0]) == ord(node2.data[0]) + 1 and int(node1.data[1]) == int(node2.data[1]) + 2:  # left 1, down 2 / right 1, up 2
                edges.append((node1.data, node2.data))
                node1.connections.append(node2.data)
                node2.connections.append(node1.data)

            elif ord(node1.data[0]) == ord(node2.data[0]) + 1 and int(node1.data[1]) == int(node2.data[1]) - 2:  # left 1, up 2 / right 1, down 2
                edges.append((node1.data, node2.data))
                node1.connections.append(node2.data)
                node2.connections.append(node1.data)

    return edges


def bishop_connections(nodes):  #if the difference between the two node's letters is the same as the difference between their numbers, its valid
    edges = []
    for node1 in nodes:
        for node2 in nodes:
            if ord(node1.data[0]) - ord(node2.data[0]) == int(node1.data[1]) - int(node2.data[1]):  # bottom left to top right
                edges.append((node1.data, node2.data))
                node1.connections.append(node2.data)
                node2.connections.append(node1.data)

            elif ord(node1.data[0]) - ord(node2.data[0]) == int(node2.data[1]) - int(node1.data[1]):  # top left to bottom right
                edges.append((node1.data, node2.data))
                node1.connections.append(node2.data)
                node2.connections.append(node1.data)



    return edges


def queen_connections(nodes):
    edges = []
    for node1 in nodes:
        for node2 in nodes:
            if node1.data[0] == node2.data[0] or node1.data[1] == node2.data[1]:  # left/right or up/down
                edges.append((node1.data, node2.data))
                node1.connections.append(node2.data)
                node2.connections.append(node1.data)

            elif ord(node1.data[0]) - ord(node2.data[0]) == int(node1.data[1]) - int(node2.data[1]):  # diagonal bottom left to top right
                edges.append((node1.data, node2.data))
                node1.connections.append(node2.data)
                node2.connections.append(node1.data)

            elif ord(node1.data[0]) - ord(node2.data[0]) == int(node2.data[1]) - int(node1.data[1]):  # diagonal top left to bottom right
                edges.append((node1.data, node2.data))
                node1.connections.append(node2.data)
                node2.connections.append(node1.data)

    return edges


def create_graph(nodes, piece):
    my_graph = nx.Graph()

    if piece == 'king':
        edges = king_connections(nodes)
    elif piece == 'rook':
        edges = rook_connections(nodes)
    elif piece == 'knight':
        edges = knight_connections(nodes)
    elif piece == 'bishop':
        edges = bishop_connections(nodes)
    elif piece == 'queen':
        edges = queen_connections(nodes)
    else:
        print('Invalid input.')
        return None

    my_graph.add_edges_from(edges)

    nx.draw(my_graph, with_labels=True)
    plt.show()
    plt.savefig('testgraph.svg')


def shortest_path(nodes, start, target):

    distance = {}
    previous = {}

    for node in nodes:
        if node.data == start:
            distance[node.data] = 0
        else:
            distance[node.data] = float('infinity')

    while nodes:
        nodes = sorted(nodes, key=lambda node:distance[node.data])
        current_node = nodes.pop(0)
        print('Analysing node:', current_node.data)

        for neighbour in current_node.connections:
            temp = distance[current_node.data] + 1
            if temp < distance[neighbour]:
                distance[neighbour] = temp
                previous[neighbour] = current_node.data


    solution = []
    current_node = target

    if previous[current_node]:
        while current_node:
            solution.insert(0, current_node)
            current_node = previous.get(current_node)

    print('Solution:', solution)


my_nodes = create_nodes()

my_piece = input('Enter chess piece: ')
start_node = input('Enter start square: ')
end_node = input('Enter end square: ')

create_graph(my_nodes, my_piece)

try:
    shortest_path(my_nodes, start_node, end_node)
except:
    print('Not a possible move for the', my_piece)


