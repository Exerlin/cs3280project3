#!/usr/bin/env python3
'''
Main script.
'''

import multiprocessing as mp
import sys
import socket

__author__ = "Ethan Jensen"
__version__ = "Fall 2020"

def scan(ip_address, start_port, end_port):
    '''
    scan(ip_address, start_port, end_port) that returns a string
    Launches processes that check for open ports within the port range given.
    Returns the cumulative result.
    '''
    queue = mp.Queue()
    number_of_ports = 1 + int(end_port) - int(start_port)
    processes = [mp.Process(target=check_for_open_port, \
        args=(ip_address, str(int(start_port) + x), queue)) for x in range(number_of_ports)]

    for process in processes:
        process.start()

    for process in processes:
        process.join()

    output_string = ""
    if queue.empty():
        output_string = "No ports within the specified range are open."
    else:
        output_string = "Open ports:"
        while not queue.empty():
            output_string += "\n" + str(queue.get())
    return output_string

def check_for_open_port(ip_address, port, queue):
    '''
    check_for_open_port(ip_address, port, queue)
    Checks if there is an open port on the given IP address with the
    given port.
    Adds the port to the queue if it is open.
    '''
    socket_to_check = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = socket_to_check.connect_ex((ip_address, int(port)))
    if result == 0:
        queue.put(port)
    socket_to_check.close()

def main():
    '''
    Launch method
    '''
    if len(sys.argv) == 4:
        print(scan(sys.argv[1], sys.argv[2], sys.argv[3]))
    else:
        print(scan(sys.argv[1], sys.argv[2], sys.argv[2]))

if __name__ == "__main__":
    main()
