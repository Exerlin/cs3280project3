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
    queue = mp.Queue()
    number_of_ports = 1 + int(end_port) - int(start_port) 
    processes = [mp.Process(target=check_for_open_port, args=(ip_address, str(int(start_port) + x), queue)) for x in range(number_of_ports)]

    list_of_results = []
    for process in processes:
        process.start()

    for process in processes:
        process.join()

    if queue.empty():
        print("No ports within the specified range are open.")
    else:
        print("Open ports:")
        for port in queue.get():
            print("\n" + str(port))

def check_for_open_port(ip_address, port, queue):
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
        scan(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        scan(sys.argv[1], sys.argv[2], sys.argv[2])

if __name__ == "__main__":
    main()
