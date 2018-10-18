#!/usr/bin/python
"""
Retrieves and collects data from the the NetApp E-series web server
and sends the data to a graphite server
"""
import struct
import time
import logging
import socket
import argparse
import concurrent.futures
import requests
import json

try:
    import cPickle as pickle
except ImportError:
    import pickle

__author__ = 'kevin5'


#######################
# LIST OF METRICS######
#######################

VOLUME_PARAMETERS = [
    'averageReadOpSize',
    'averageWriteOpSize',
    'combinedIOps',
    'combinedResponseTime',
    'combinedThroughput',
    'flashCacheHitPct',
    'flashCacheReadHitBytes',
    'flashCacheReadHitOps',
    'flashCacheReadResponseTime',
    'flashCacheReadThroughput',
    'otherIOps',
    'queueDepthMax',
    'queueDepthTotal',
    'readCacheUtilization',
    'readHitBytes',
    'readHitOps',
    'readIOps',
    'readOps',
    'readPhysicalIOps',
    'readResponseTime',
    'readThroughput',
    'writeCacheUtilization',
    'writeHitBytes',
    'writeHitOps',
    'writeIOps',
    'writeOps',
    'writePhysicalIOps',
    'writeResponseTime',
    'writeThroughput'
]

DRIVE_PARAMETERS = [
    'averageReadOpSize',
    'averageWriteOpSize',
    'combinedIOps',
    'combinedResponseTime',
    'combinedThroughput',
    'otherIOps',
    'readIOps',
    'readOps',
    'readPhysicalIOps',
    'readResponseTime',
    'readThroughput',
    'writeIOps',
    'writeOps',
    'writePhysicalIOps',
    'writeResponseTime',
    'writeThroughput'
]


#######################
# PARAMETERS###########
#######################

NUMBER_OF_THREADS = 10

# LOGGING
logging.basicConfig(level=logging.INFO)
requests.packages.urllib3.disable_warnings()
LOG = logging.getLogger(__name__)

# Disables reset connection warning message if the connection time is too long
logging.getLogger('requests.packages.urllib3.connectionpool').setLevel(logging.WARNING)


#######################
# ARGUMENT PARSER######
#######################

PARSER = argparse.ArgumentParser()

PARSER.add_argument('-t', '--intervalTime', type=int, default=5,
                    help='Provide the time (seconds) in which the script polls and sends data '
                         'from the SANtricity webServer to the Graphite backend. '
                         'If not specified, will use the default time of 60 seconds. <time>')
PARSER.add_argument('-r', '--root', default='storage.eseries',
                    help='the metrics root to place onto Graphite. The default is storage.eseries '
                         'as to match the given Grafana templates. If this is changed, '
                         'you must also manually change the Grafana templates. '
                         '<period separated list>')
PARSER.add_argument('--proxySocketAddress', default='webservices',
                    help='Provide both the IP address and the port for the SANtricity webserver. '
                         'If not specified, will default to localhost. <IPv4 Address:port>')
PARSER.add_argument('--graphiteIpAddress', default='graphite',
                    help='Provide the IP address of the graphite server. If not specified, '
                         'will default to localhost. <IPv4 Address>')
PARSER.add_argument('--graphitePort', type=int, default=2004,
                    help='Provide the port number used for the graphite backend (Carbon).'
                         ' When Graphite is installed, by default this is port is 2004.'
                         ' If this parameter is not specified, this will default to 2004 <port>')
PARSER.add_argument('-s', '--showStorageNames', action='store_true',
                    help='Outputs the storage array names found from the SANtricity webserver')
PARSER.add_argument('-v', '--showVolumeNames', action='store_true', default=0,
                    help='Outputs the volume names found from the SANtricity webserver')
PARSER.add_argument('-a', '--showVolumeMetrics', action='store_true', default=0,
                    help='Outputs the volume payload metrics before it is sent')
PARSER.add_argument('-d', '--showDriveNames', action='store_true', default=0,
                    help='Outputs the drive names found from the SANtricity webserver')
PARSER.add_argument('-b', '--showDriveMetrics', action='store_true', default=0,
                    help='Outputs the drive payload metrics before it is sent')
PARSER.add_argument('-i', '--showIteration', action='store_true', default=0,
                    help='Outputs the current loop iteration')
PARSER.add_argument('-n', '--doNotPost', action='store_true', default=0,
                    help='Pull information, but do not post to graphite')
CMD = PARSER.parse_args()
PROXY_BASE_URL = 'http://{}/devmgr/v2/storage-systems'.format(CMD.proxySocketAddress)


#######################
# HELPER FUNCTIONS#####
#######################

def get_session():
    """
    Returns a session with the appropriate content type and login information.
    :return: Returns a request session for the SANtricity RestAPI Webserver
    """
    request_session = requests.Session()

    # Try to read username and password from config file, if it exists
    # Otherwise default to admin/admin
    try:
        with open('config.json') as config_file:
            config_data = json.load(config_file)
            if (config_data):
                USERNAME = config_data["username"]
                PASSWORD = config_data["password"]
    except:
        LOG.info("Unable to open \'/collector/config.json\' file")
        USERNAME = "admin"
        PASSWORD = "admin"

    request_session.auth = (USERNAME, PASSWORD)
    request_session.headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
    # Ignore the self-signed certificate issues for https
    request_session.verify = False
    return request_session

def post_to_graphite(system_id, graphite_metrics):
    """
    Posts the graphite metrics to carbon (graphite's backend).
    """
    LOG.info("Sending to graphite, points=%s, system=%s", len(graphite_metrics), system_id)
    chunk_size = 400
    chunks = [graphite_metrics[x:x+chunk_size] for x in range(0, len(graphite_metrics), chunk_size)]
    LOG.debug("Sending %s chunks for system=%s.", len(chunks), system_id)
    for data in chunks:
        payload = pickle.dumps(data, protocol=2)
        header = struct.pack("!L", len(payload))
        message = header + payload
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as graphite_server:
            graphite_server.connect((CMD.graphiteIpAddress, CMD.graphitePort))
            bytesSent = graphite_server.send(message)
            LOG.debug("\t%s bytes sent", bytesSent)
            graphite_server.close()

def get_drive_location(storage_id, session):
    """
    :param storage_id: Storage system ID on the Webserver
    :param session: the session of the thread that calls this definition
    ::return: returns a dictionary containing the disk id matched up against
    the tray id it is located in:
    """
    hardware_list = session.get('{}/{}/hardware-inventory'.format(
        PROXY_BASE_URL, storage_id)).json()
    tray_list = hardware_list['trays']
    drive_list = hardware_list['drives']
    tray_ids = {}
    drive_location = {}

    for tray in tray_list:
        tray_ids[tray['trayRef']] = tray['trayId']

    for drive in drive_list:
        drive_tray = drive['physicalLocation']['trayRef']
        tray_id = tray_ids.get(drive_tray)
        if tray_id != 'none':
            drive_location[drive['driveRef']] = [tray_id, drive['physicalLocation']['slot']]
        else:
            LOG.error('Error matching drive to a tray in the storage system')
    return drive_location

def collect_storage_system_statistics(storage_system):
    """
    Collects and sends statistics of a single storage system to graphite.
    :param storage_system: The JSON object of a storage_system
    """
    try:
        session = get_session()
        graphite_package = []
        storage_id = storage_system['id']
        storage_name = storage_system.get('name', storage_id)
        drives = session.get('{}/{}/drives'.format(
            PROXY_BASE_URL, storage_id)).json()
        # Get Drive statistics
        graphite_drive_root = (('{}.{}.drive_statistics'.format(
            CMD.root, storage_name)))
        drive_stats_list = session.get('{}/{}/analysed-drive-statistics'.format(
            PROXY_BASE_URL, storage_id)).json()
        drive_locations = get_drive_location(storage_id, session)

        if CMD.showDriveNames:
            for driveStats in drive_stats_list:
                location_send = drive_locations.get(driveStats['diskId'])
                LOG.info('tray{:02.0f}.slot{:03.0f}'.format(location_send[0], location_send[1]))

        # Add drive statistics to list
        for driveStats in drive_stats_list:
            for metricsToCheck in DRIVE_PARAMETERS:
                if driveStats.get(metricsToCheck) != 'none':
                    location_send = drive_locations.get(driveStats['diskId'])
                    graphite_payload = ('{}.Tray-{:02.0f}.Disk-{:03.0f}.{}'.format(
                        graphite_drive_root,
                        location_send[0],
                        location_send[1],
                        metricsToCheck), (int(time.time()), driveStats.get(metricsToCheck)))
                    if CMD.showDriveMetrics:
                        LOG.info(graphite_payload)
                    graphite_package.append(graphite_payload)
                    # With pool information
                    graphite_payload = ('{}.Tray-{:02.0f}.Disk-{:03.0f}.{}'.format(
                        graphite_drive_root,
                        location_send[0],
                        location_send[1],
                        metricsToCheck), (int(time.time()), driveStats.get(metricsToCheck)))
                    if CMD.showDriveMetrics:
                        LOG.info(graphite_payload)
                    graphite_package.append(graphite_payload)

        # Get Volume statistics
        graphite_volume_root = ('{}.{}.volume_statistics'.format(
            CMD.root, storage_name))
        volume_stats_list = session.get('{}/{}/analysed-volume-statistics'.format(
            PROXY_BASE_URL, storage_id)).json()

        if CMD.showVolumeNames:
            for volumeStats in volume_stats_list:
                LOG.info(volumeStats['volumeName'])

        # Add volume statistics to list
        for volumeStats in volume_stats_list:
            for metricsToCheck in VOLUME_PARAMETERS:
                this_metric = volumeStats.get(metricsToCheck)
                if this_metric is not None:
                    graphite_payload = ('{}.{}.{}'.format(
                        graphite_volume_root,
                        volumeStats.get('volumeName'),
                        metricsToCheck), (int(time.time()), this_metric))
                    if CMD.showVolumeMetrics:
                        LOG.debug(graphite_payload)
                    graphite_package.append(graphite_payload)

        if not CMD.doNotPost:
            post_to_graphite(storage_id, graphite_package)
    except RuntimeError:
        LOG.error('Error when attempting to post statistics for {}'.format(
            storage_system['name']))


#######################
# MAIN FUNCTIONS#######
#######################

if __name__ == '__main__':
    executor = concurrent.futures.ProcessPoolExecutor(NUMBER_OF_THREADS)
    SESSION = get_session()
    loopIteration = 1

    while True:
        time_start = time.time()
        try:
            response = SESSION.get(PROXY_BASE_URL)
            if response.status_code != 200:
                LOG.warning("We were unable to retrieve the storage-system list! Status-code={}".format(response.status_code))
        except requests.exceptions.HTTPError or requests.exceptions.ConnectionError as e:
            LOG.warning("Unable to connect to the Web Services instance to get storage-system list!", e)
        except Exception as e:
            LOG.warning("Unexpected exception!", e)
        else:
            storageList = response.json()
            LOG.info("Names: %s", len(storageList))
            if CMD.showStorageNames:
                for storage in storageList:
                    LOG.info(storage['name'])

            # Iterate through all storage systems
            collector = [executor.submit(collect_storage_system_statistics, s) for s in storageList]
            concurrent.futures.wait(collector)

        time_difference = time.time() - time_start
        if CMD.showIteration:
            LOG.info('Time interval: {:07.4f} Time to collect and send:'
                     ' {:07.4f} Iteration: {:00.0f}'
                     .format(CMD.intervalTime, time_difference, loopIteration))
            loopIteration += 1

        # Dynamic wait time to get the proper interval
        if CMD.intervalTime < time_difference:
            LOG.error('The interval specified is not long enough. Time used: {:07.4f} '
                      'Time interval specified: {:07.4f}'
                      .format(time_difference, CMD.intervalTime))
        time.sleep(CMD.intervalTime - time_difference)
