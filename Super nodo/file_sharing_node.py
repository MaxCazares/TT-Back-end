import sys
from FileSharingNode import FileSharingNode
import hashlib

# The method prints the help commands text to the console


def print_help():
    print("stop - Stops the application.")
    print("help - Prints this help text.")


def connect_to_node(node: FileSharingNode):
    host = input("Node ip > ")
    port = int(input("port > "))
    node.connect_with_node(host, port)


def send_messages(message):
    node.send_to_nodes({"message": message})


def send_message(message):
    node.send_to_node(node.super_par, message)


if len(sys.argv) != 2:
    print('A port number is required')
else:
    port = int(sys.argv[1])

    # Instantiate the node FileSharingNode, it creates a thread to handle all functionality
    node = FileSharingNode('0.0.0.0', port)

    # Start the node, if not started it shall not handle any requests!
    node.start()

    # Implement a console application
    command = input("> ")
    while (command != "stop"):
        if (command == "help"):
            print_help()
        if (command == "connect"):
            connect_to_node(node)
        if (command == 'message'):
            m = input('\t # ')
            send_messages(m)

        command = input("> ")

    node.stop()
