#!/usr/bin/python

import random
import socket
import struct

import time

SERVER = 'localhost'
PORT = 2004

try:
    import cPickle as pickle
except ImportError:
    import pickle

def main():
    # These are sample metrics
    metrics = ['test.' + str(i) for i in range(10)]

    i = 0
    while(True):
        print('Iteration %s: Sending metrics' % i)

        # current time in seconds since epoch
        timestamp = time.time()

        # This is a list containing multi-level tuples (see below).
        listOfMetricTuples = list()

        for metric in metrics:
            # This is a tuple of the form: (path, (timestamp, value))
            # Generally, we want to keep the number of metrics per call to < 500 (without special tuning of Graphite)
            data_point = (metric, (timestamp, random.randint(0, 1000)))
            listOfMetricTuples.append(data_point)

        send_to_graphite(listOfMetricTuples)
        time.sleep(5)
        i += 1


def send_to_graphite(listOfMetricTuples):
    payload = pickle.dumps(listOfMetricTuples, protocol=2)
    header = struct.pack("!L", len(payload))
    message = header + payload
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as graphite_server:
        graphite_server.connect((SERVER, PORT))
        graphite_server.send(message)
        graphite_server.close()


if __name__ == '__main__':
    main()
