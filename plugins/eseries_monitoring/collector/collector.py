#!/usr/bin/python
"""
Retrieves and collects data from the the NetApp E-series web server
and sends the data to an influxdb server
"""
import struct
import time
import logging
import socket
import argparse
import concurrent.futures
import requests
import json
import hashlib
from datetime import datetime

from datetime import datetime
from influxdb import InfluxDBClient
from influxdb.exceptions import InfluxDBClientError

try:
    import cPickle as pickle
except ImportError:
    import pickle

DEFAULT_USERNAME = 'admin'
DEFAULT_PASSWORD = 'admin'

DEFAULT_SYSTEM_NAME = 'unnamed'

INFLUXDB_HOSTNAME = 'influxdb'
INFLUXDB_PORT = 8086
INFLUXDB_DATABASE = 'eseries'

# NOTE(bdustin): time in seconds between folder collections
FOLDER_COLLECTION_INTERVAL = 60*10

__version__ = '1.0'

#######################
# LIST OF METRICS######
#######################

DRIVE_PARAMS = [
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

SYSTEM_PARAMS = [
    "maxCpuUtilization",
    "cpuAvgUtilization"
]

VOLUME_PARAMS = [
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

MEL_PARAMS = [
    'id',
    'description',
    'location'
]


#######################
# PARAMETERS###########
#######################

NUMBER_OF_THREADS = 10

# LOGGING
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
requests.packages.urllib3.disable_warnings()
LOG = logging.getLogger("collector")

# Disables reset connection warning message if the connection time is too long
logging.getLogger('requests.packages.urllib3.connectionpool').setLevel(logging.WARNING)


#######################
# ARGUMENT PARSER######
#######################

PARSER = argparse.ArgumentParser()

PARSER.add_argument('-u', '--username', default='',
                    help='Provide the username used to connect to the Web Services Proxy. '
                         'If not specified, will check for the \'/collector/config.json\' file. '
                         'Otherwise, it will default to \'' + DEFAULT_USERNAME + '\'')
PARSER.add_argument('-p', '--password', default='',
                    help='Provide the password for this user to connect to the Web Services Proxy. '
                         'If not specified, will check for the \'/collector/config.json\' file. '
                         'Otherwise, it will default to \'' + DEFAULT_PASSWORD + '\'')
PARSER.add_argument('-t', '--intervalTime', type=int, default=5,
                    help='Provide the time (seconds) in which the script polls and sends data '
                         'from the SANtricity webserver to the influxdb backend. '
                         'If not specified, will use the default time of 60 seconds. <time>')
PARSER.add_argument('--proxySocketAddress', default='webservices',
                    help='Provide both the IP address and the port for the SANtricity webserver. '
                         'If not specified, will default to localhost. <IPv4 Address:port>')
PARSER.add_argument('-r', '--retention', type=str, default='52w',
                    help='The default retention duration for influxdb')
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
PARSER.add_argument('-c', '--showSystemMetrics', action='store_true', default=0,
                    help='Outputs the system payload metrics before it is sent')
PARSER.add_argument('-m', '--showMELMetrics', action='store_true', default=0,
                    help='Outputs the MEL payload metrics before it is sent')
PARSER.add_argument('-e', '--showStateMetrics', action='store_true', default=0,
                    help='Outputs the state payload metrics before it is sent')
PARSER.add_argument('-i', '--showIteration', action='store_true', default=0,
                    help='Outputs the current loop iteration')
PARSER.add_argument('-n', '--doNotPost', action='store_true', default=0,
                    help='Pull information, but do not post to influxdb')
CMD = PARSER.parse_args()
PROXY_BASE_URL = 'http://{}/devmgr/v2/storage-systems'.format(CMD.proxySocketAddress)
RETENTION_DUR = CMD.retention

#######################
# HELPER FUNCTIONS#####
#######################

def get_configuration():
    try:
        with open("config.json") as config_file:
            config_data = json.load(config_file)
            if config_data:
                return config_data
    except:
        return dict()


def get_session():
    """
    Returns a session with the appropriate content type and login information.
    :return: Returns a request session for the SANtricity RestAPI Webserver
    """
    request_session = requests.Session()

    # Try to use what was passed in for username/password...
    username = CMD.username
    password = CMD.password
    
    # ...if there was nothing passed in then try to read it from config file
    if ((username is None or username == "") and (password is None or password == "")):
        # Try to read username and password from config file, if it exists
        # Otherwise default to DEFAULT_USERNAME/DEFAULT_PASSWORD
        try:
            with open("config.json") as config_file:
                config_data = json.load(config_file)
                if (config_data):
                    username = config_data["username"]
                    password = config_data["password"]
        except:
            LOG.exception("Unable to open \"/collector/config.json\" file")
            username = DEFAULT_USERNAME
            password = DEFAULT_PASSWORD

    request_session.auth = (username, password)
    request_session.headers = {"Accept": "application/json",
                               "Content-Type": "application/json",
                               "netapp-client-type": "grafana-" + __version__}
    # Ignore the self-signed certificate issues for https
    request_session.verify = False
    return request_session


def get_drive_location(storage_id, session):
    """
    :param storage_id: Storage system ID on the Webserver
    :param session: the session of the thread that calls this definition
    ::return: returns a dictionary containing the disk id matched up against
    the tray id it is located in:
    """
    hardware_list = session.get("{}/{}/hardware-inventory".format(
        PROXY_BASE_URL, storage_id)).json()
    tray_list = hardware_list["trays"]
    drive_list = hardware_list["drives"]
    tray_ids = {}
    drive_location = {}

    for tray in tray_list:
        tray_ids[tray["trayRef"]] = tray["trayId"]

    for drive in drive_list:
        drive_tray = drive["physicalLocation"]["trayRef"]
        tray_id = tray_ids.get(drive_tray)
        if tray_id != "none":
            drive_location[drive["driveRef"]] = [tray_id, drive["physicalLocation"]["slot"]]
        else:
            LOG.error("Error matching drive to a tray in the storage system")
    return drive_location

def collect_storage_metrics(sys):
    """
    Collects all defined storage metrics and posts them to influxdb
    :param sys: The JSON object of a storage_system
    """
    try:
        session = get_session()
        client = InfluxDBClient(host=INFLUXDB_HOSTNAME, port=INFLUXDB_PORT, database=INFLUXDB_DATABASE)

        sys_id = sys["id"]
        sys_name = sys.get("name", sys_id)
        # If this storage device lacks a name, use the id
        if not sys_name or len(sys_name) <= 0:
            sys_name = sys_id
        # If this storage device still lacks a name, use a default
        if not sys_name or len(sys_name) <= 0:
            sys_name = DEFAULT_SYSTEM_NAME

        json_body = list()

        # Get Drive statistics
        drive_stats_list = session.get(("{}/{}/analysed-drive-statistics").format(
            PROXY_BASE_URL, sys_id)).json()
        drive_locations = get_drive_location(sys_id, session)
        if CMD.showDriveNames:
            for stats in drive_stats_list:
                location_send = drive_locations.get(stats["diskId"])
                LOG.info(("Tray{:02.0f}, Slot{:03.0f}").format(location_send[0], location_send[1]))
        # Add Drive statistics to json body
        for stats in drive_stats_list:
            disk_location_info = drive_locations.get(stats["diskId"])
            disk_item = dict(
                measurement = "disks",
                tags = dict(
                    sys_id = sys_id,
                    sys_name = sys_name,
                    sys_tray = ("{:02.0f}").format(disk_location_info[0]),
                    sys_tray_slot = ("{:03.0f}").format(disk_location_info[1])
                ),
                fields = dict(
                    (metric, stats.get(metric)) for metric in DRIVE_PARAMS
                )
            )
            if CMD.showDriveMetrics:
                LOG.info("Drive payload: %s", disk_item)
            json_body.append(disk_item)

        # Get System statistics
        system_stats_list = session.get(("{}/{}/analysed-system-statistics").format(
            PROXY_BASE_URL, sys_id)).json()
        # Add System statistics to json body
        sys_item = dict(
            measurement = "systems",
            tags = dict(
                sys_id = sys_id,
                sys_name = sys_name
            ),
            fields = dict(
                (metric, system_stats_list.get(metric)) for metric in SYSTEM_PARAMS
            )
        )
        if CMD.showSystemMetrics:
            LOG.info("System payload: %s", sys_item)
        json_body.append(sys_item)
        
        # Get Volume statistics
        volume_stats_list = session.get(("{}/{}/analysed-volume-statistics").format(
            PROXY_BASE_URL, sys_id)).json()
        if CMD.showVolumeNames:
            for stats in volume_stats_list:
                LOG.info(stats["volumeName"])
        # Add Volume statistics to json body
        for stats in volume_stats_list:
            vol_item = dict(
                measurement = "volumes",
                tags = dict(
                    sys_id = sys_id,
                    sys_name = sys_name,
                    vol_name = stats["volumeName"]
                ),
                fields = dict(
                    (metric, stats.get(metric)) for metric in VOLUME_PARAMS
                )
            )
            if CMD.showVolumeMetrics:
                LOG.info("Volume payload: %s", vol_item)
            json_body.append(vol_item)

        if not CMD.doNotPost:
            client.write_points(json_body, database=INFLUXDB_DATABASE, time_precision="s")

    except RuntimeError:
        LOG.error(("Error when attempting to post statistics for {}/{}").format(sys["name"], sys["id"]))


def collect_major_event_log(sys):
    """
    Collects all defined MEL metrics and posts them to influxdb
    :param sys: The JSON object of a storage_system
    """
    try:
        session = get_session()
        client = InfluxDBClient(host=INFLUXDB_HOSTNAME, port=INFLUXDB_PORT, database=INFLUXDB_DATABASE)
        
        sys_id = sys["id"]
        sys_name = sys.get("name", sys_id)
        # If this storage device lacks a name, use the id
        if not sys_name or len(sys_name) <= 0:
            sys_name = sys_id
        # If this storage device still lacks a name, use a default
        if not sys_name or len(sys_name) <= 0:
            sys_name = DEFAULT_SYSTEM_NAME
        
        json_body = list()
        start_from = -1
        mel_grab_count = 8192
        query = client.query("SELECT id FROM major_event_log WHERE sys_id='%s' ORDER BY time DESC LIMIT 1" % sys_id)

        if query:
            start_from = int(next(query.get_points())["id"]) + 1
        
        mel_response = session.get(("{}/{}/mel-events").format(PROXY_BASE_URL, sys_id),
                                   params = {"count": mel_grab_count, "startSequenceNumber": start_from}, timeout=(6.10, CMD.intervalTime*2)).json()
        if CMD.showMELMetrics:
            LOG.info("Starting from %s", str(start_from))
            LOG.info("Grabbing %s MELs", str(len(mel_response)))
        for mel in mel_response:
            item = dict(
                measurement = "major_event_log",
                tags = dict(
                    sys_id = sys_id,
                    sys_name = sys_name,
                    event_type = mel["eventType"],
                    time_stamp = mel["timeStamp"],
                    category = mel["category"],
                    priority = mel["priority"],
                    critical = mel["critical"],
                    ascq = mel["ascq"],
                    asc = mel["asc"]
                ),
                fields = dict(
                    (metric, mel.get(metric)) for metric in MEL_PARAMS
                ),
                time = datetime.utcfromtimestamp(int(mel["timeStamp"])).isoformat()
            )
            if CMD.showMELMetrics:
                LOG.info("MEL payload: %s", item)
            json_body.append(item)
        
        client.write_points(json_body, database=INFLUXDB_DATABASE, time_precision="s")
    except RuntimeError:
        LOG.error(("Error when attempting to post MEL for {}/{}").format(sys["name"], sys["id"]))


def create_failure_dict_item(sys_id, sys_name, fail_type, obj_ref, obj_type, is_active, the_time):
    item = dict(
        measurement = "failures",
        tags = dict(
            sys_id = sys_id,
            sys_name = sys_name,
            failure_type = fail_type,
            object_ref = obj_ref,
            object_type = obj_type,
            active = is_active
        ),
        fields = dict(
            name_of = sys_name,
            type_of = fail_type
        ),
        time = the_time
    )
    return item

def collect_system_state(sys, checksums):
    """
    Collects state information from the storage system and posts it to influxdb
    :param sys: The JSON object of a storage_system
    """
    try:
        session = get_session()
        client = InfluxDBClient(host=INFLUXDB_HOSTNAME, port=INFLUXDB_PORT, database=INFLUXDB_DATABASE)
        
        sys_id = sys["id"]
        sys_name = sys.get("name", sys_id)
        # If this storage device lacks a name, use the id
        if not sys_name or len(sys_name) <= 0:
            sys_name = sys_id
        # If this storage device still lacks a name, use a default
        if not sys_name or len(sys_name) <= 0:
            sys_name = DEFAULT_SYSTEM_NAME

        # query the api and get a list of current failures for this system
        failure_response = session.get(("{}/{}/failures").format(PROXY_BASE_URL, sys_id)).json()

        # we can skip us if this is the same response we handled last time
        old_checksum = checksums.get(str(sys_id))
        new_checksum = hashlib.md5(str(failure_response).encode("utf-8")).hexdigest()
        if old_checksum is not None and str(new_checksum) == str(old_checksum):
            return
        checksums.update({str(sys_id) : str(new_checksum)})

        # pull most recent failures for this system from our database, including their active status
        query_string = ("SELECT last(\"type_of\"),failure_type,object_ref,object_type,active FROM \"failures\" WHERE (\"sys_id\" = '{}') GROUP BY \"sys_name\", \"failure_type\"").format(sys_id)
        query = client.query(query_string)
        failure_points = list(query.get_points())

        json_body = list()

        # take care of active failures we don't know about
        for failure in failure_response:
            r_fail_type = failure.get("failureType")
            r_obj_ref = failure.get("objectRef")
            r_obj_type = failure.get("objectType")
            
            # we push if we haven't seen this, or we think it's inactive
            push = True
            for point in failure_points:
                p_fail_type = point["failure_type"]
                p_obj_ref = point["object_ref"]
                p_obj_type = point["object_type"]
                p_active = point["active"]
                if (r_fail_type == p_fail_type
                    and r_obj_ref == p_obj_ref
                    and r_obj_type == p_obj_type):
                    if p_active == "True":
                        push = False # we already know this is an active failure so don't push
                    break

            if push:
                if CMD.showStateMetrics:
                    LOG.info("Failure payload T1: %s", item)
                json_body.append(create_failure_dict_item(sys_id, sys_name,
                                                          r_fail_type, r_obj_ref, r_obj_type,
                                                          True, datetime.utcnow().isoformat()))

        # take care of failures that are no longer active
        for point in failure_points:
            # we only care about points that we think are active
            p_active = point["active"]
            if not p_active:
                continue

            p_fail_type = point["failure_type"]
            p_obj_ref = point["object_ref"]
            p_obj_type = point["object_type"]
            
            # we push if we are no longer active, but think that we are
            push = True
            for failure in failure_response:
                r_fail_type = failure.get("failureType")
                r_obj_ref = failure.get("objectRef")
                r_obj_type = failure.get("objectType")
                if (r_fail_type == p_fail_type
                    and r_obj_ref == p_obj_ref
                    and r_obj_type == p_obj_type):
                    push = False # we are still active, so don't push
                    break

            if push:
                if CMD.showStateMetrics:
                    LOG.info("Failure payload T2: %s", item)
                json_body.append(create_failure_dict_item(sys_id, sys_name,
                                                          p_fail_type, p_obj_ref, p_obj_type,
                                                          False, datetime.utcnow().isoformat()))
                
        # write failures to influxdb
        if CMD.showStateMetrics:
            LOG.info("Writing {} failures".format(len(json_body)))
        client.write_points(json_body, database=INFLUXDB_DATABASE)

    except RuntimeError:
        LOG.error(("Error when attempting to post state information for {}/{}").format(sys["name"], sys["id"]))

def create_continuous_query(params_list, database):
    try:
        for metric in params_list:
            ds_select = "SELECT mean(\"" + metric + "\") AS \"ds_" + metric + "\" INTO \"" + INFLUXDB_DATABASE + "\".\"downsample_retention\".\"" + database + "\" FROM \"" + database + "\" WHERE (time < now()-1w) GROUP BY time(5m)"
            #LOG.info(ds_select)
            client.create_continuous_query("downsample_" + database + "_" + metric, ds_select, INFLUXDB_DATABASE, "")
            #client.drop_continuous_query("downsample_" + database + "_" + metric, INFLUXDB_DATABASE)
    except Exception as err:
        LOG.info("Creation of continuous query on '{}' failed: {}".format(database, err))

def get_storage_system_ids_folder_list():
    PROXY_FOLDER_URL = ("http://{}/devmgr/v2/folders").format(CMD.proxySocketAddress)
    folder_response = SESSION.get(PROXY_FOLDER_URL).json()
    folders = list()
    for folder in folder_response:
        folder_name = folder["name"]
        subfolder = dict(
            name = folder_name,
            systemIDs = list(),
            systemNames = list()
        )
        for system in folder["storageSystemIds"]:
            subfolder["systemIDs"].append(system)
        folders.append(subfolder)

    return folders

def add_system_names_to_ids_list(folder_of_ids):
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
        for folder in folder_of_ids:
            for storage_id in folder["systemIDs"]:
                for system in storageList:
                    if (system["id"] == storage_id):
                        folder["systemNames"].append(system["name"])
                        break

        for folder in folder_of_ids:
            if (folder["name"] == "All Storage Systems"):
                for system in storageList:
                    folder["systemIDs"].append(system["id"])
                    folder["systemNames"].append(system["name"])

    return folder_of_ids

def get_storage_system_folder_list():
    folders = get_storage_system_ids_folder_list()
    return add_system_names_to_ids_list(folders)

def collect_system_folders(systems):
    """
    Collects all folders defined in the WSP and posts them to influxdb
    :param systems: List of all system folders (names and IDs)
    """
    try:
        client = InfluxDBClient(host=INFLUXDB_HOSTNAME, port=INFLUXDB_PORT, database=INFLUXDB_DATABASE)
        json_body = list()

        for folder in systems:
            for name in folder["systemNames"]:
                sys_item = dict(
                    measurement = "folders",
                    tags = dict(
                        folder_name = folder["name"],
                        sys_name = name
                    ),
                    fields = dict(
                        dummy = 0
                    )
                )
                json_body.append(sys_item)
        if not CMD.doNotPost:
            client.drop_measurement("folders")
            client.write_points(json_body, database=INFLUXDB_DATABASE, time_precision="s")

    except RuntimeError:
        LOG.error("Error when attempting to post system folders")
  
#######################
# MAIN FUNCTIONS#######
#######################

if __name__ == "__main__":
    executor = concurrent.futures.ThreadPoolExecutor(NUMBER_OF_THREADS)
    SESSION = get_session()
    loopIteration = 1

    client = InfluxDBClient(host=INFLUXDB_HOSTNAME, port=INFLUXDB_PORT, database=INFLUXDB_DATABASE)

    client.create_database(INFLUXDB_DATABASE)

    try:
        # Ensure we can connect. Wait for 2 minutes for WSP to startup.
        SESSION.get(PROXY_BASE_URL, timeout=120)
        configuration = get_configuration()

        # set up our default retention policies if we have that configured
        try:
            client.create_retention_policy("default_retention", "1w", "1", INFLUXDB_DATABASE, True)
        except InfluxDBClientError:
            LOG.info("Updating retention policy to {}...".format("1w"))
            client.alter_retention_policy("default_retention", INFLUXDB_DATABASE,
                                          "1w", "1", True)
        try:
            client.create_retention_policy("downsample_retention", RETENTION_DUR, "1", INFLUXDB_DATABASE, False)
        except InfluxDBClientError:
            LOG.info("Updating retention policy to {}...".format(RETENTION_DUR))
            client.alter_retention_policy("downsample_retention", INFLUXDB_DATABASE,
                                          RETENTION_DUR, "1", False)
        
        # set up continuous queries that will downsample our metric data periodically
        create_continuous_query(DRIVE_PARAMS, "disks")
        create_continuous_query(SYSTEM_PARAMS, "system")
        create_continuous_query(VOLUME_PARAMS, "volumes")
    
        for system in configuration.get("storage_systems", list()):
            LOG.info("system: %s", str(system))
            body = dict(controllerAddresses=system.get("addresses"),
                        password=system.get("password") or configuration.get("array_password"),
                        acceptCertificate=True)
            response = SESSION.post(PROXY_BASE_URL, json=body)
            response.raise_for_status()
    except requests.exceptions.HTTPError or requests.exceptions.ConnectionError:
        LOG.exception("Failed to add configured systems!")
    except json.decoder.JSONDecodeError:
        LOG.exception("Failed to open configuration file due to invalid JSON!")

    # Time that we last collected array folder information
    last_folder_collection = -1

    checksums = dict()
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
                    storage_name = storage["name"]
                    if not storage_name or len(storage_name) <= 0:
                        storage_name = storage["id"]
                    if not storage_name or len(storage_name) <= 0:
                        storage_name = DEFAULT_STORAGE_NAME
                    LOG.info(storage_name)

            # Grab array folders and commit the data to InfluxDB
            if (last_folder_collection < 0 or time.time() - last_folder_collection >= FOLDER_COLLECTION_INTERVAL):
                LOG.info("Collecting system folder information...")
                storage_system_list = get_storage_system_folder_list()
                collect_system_folders(storage_system_list)
                last_folder_collection = time.time()

            # Iterate through all storage systems and collect metrics
            collector = [executor.submit(collect_storage_metrics, sys) for sys in storageList]
            concurrent.futures.wait(collector)

            # Iterate through all storage system and collect state information
            collector = [executor.submit(collect_system_state, sys, checksums) for sys in storageList]
            concurrent.futures.wait(collector)
            
            # Iterate through all storage system and collect MEL entries
            collector = [executor.submit(collect_major_event_log, sys) for sys in storageList]
            concurrent.futures.wait(collector)

        time_difference = time.time() - time_start
        if CMD.showIteration:
            LOG.info("Time interval: {:07.4f} Time to collect and send:"
                     " {:07.4f} Iteration: {:00.0f}"
                     .format(CMD.intervalTime, time_difference, loopIteration))
            loopIteration += 1

        # Dynamic wait time to get the proper interval
        wait_time = CMD.intervalTime - time_difference
        if CMD.intervalTime < time_difference:
            LOG.error("The interval specified is not long enough. Time used: {:07.4f} "
                      "Time interval specified: {:07.4f}"
                      .format(time_difference, CMD.intervalTime))
            wait_time = time_difference
            
        time.sleep(wait_time)
