#!/usr/bin/python
"""
Running this script will migrate performance metrics from a previous
Graphite Performance Analyzer database to the new InfluxDB database.
This is accomplished by querying the running Graphite database for 
collected metrics and generating new queries to push them to InfluxDB.
"""
import json
import logging
import requests
import argparse
import concurrent.futures

from datetime import datetime
from influxdb import InfluxDBClient


INFLUXDB_PORT = 8086
INFLUXDB_DATABASE = "eseries"


##
# Argument Parser
##
PARSER = argparse.ArgumentParser()
PARSER.add_argument("-n", "--hostname", default="localhost",
                    help="Provide the name of the host on which the services are running")
PARSER.add_argument("-u", "--grafanaUsername", default="admin",
                    help="The username used to login to Grafana")
PARSER.add_argument("-p", "--grafanaPassword", default="admin",
                    help="The password used to login to Grafana")
PARSER.add_argument("-w", "--proxyUsername", default="admin",
                    help="Provide the username used to connect to the Web Services Proxy. "
                         "If not specified, will check for the \"/collector/config.json\" file. "
                         "Otherwise, it will default to \"admin\"")
PARSER.add_argument("-a", "--proxyPassword", default="admin",
                    help="Provide the password for this user to connect to the Web Services Proxy. "
                         "If not specified, will check for the \"/collector/config.json\" file. "
                         "Otherwise, it will default to \"admin\"")
CMD = PARSER.parse_args()

QUERY_BASE_URL = ("http://{}:3000").format(CMD.hostname)
BASE_PREFIX = len("storage.eseries.")
GRAFANA_AUTH = (CMD.grafanaUsername, CMD.grafanaPassword)

##
# Logging
##
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
requests.packages.urllib3.disable_warnings()
LOG = logging.getLogger("db_migrator")

##
# Migration functions
##

def migrate_disk_metrics(sys_name, sys_id, source_uri):
    drive_stats_prefix = BASE_PREFIX + len(sys_name + ".drive_statistics.")

    session = requests.Session()
    session.auth = GRAFANA_AUTH
    client = InfluxDBClient(host=CMD.hostname, port=INFLUXDB_PORT, database=INFLUXDB_DATABASE,
                            username="admin", password="")
    influxdb_payload = list()

    trays_list = session.get(("{}/metrics/expand?query=storage.eseries.{}.drive_statistics.*&format=json").format(source_uri, sys_name)).json()
    for tray in trays_list["results"]:
        tray_name = tray[drive_stats_prefix :]
        tray_number = tray_name[5 :]
        tray_prefix = drive_stats_prefix + len(tray_name) + 1 # remove tray name and .
        slots_list = session.get(("{}/metrics/expand?query=storage.eseries.{}.drive_statistics.{}.*&format=json").format(source_uri, sys_name, tray_name)).json()
        for slot in slots_list["results"]:
            slot_name = slot[tray_prefix :]
            slot_number = slot_name[5 :]
            slot_prefix = tray_prefix + len(slot_name) + 1
            metrics_list = session.get(("{}/metrics/expand?query=storage.eseries.{}.drive_statistics.{}.{}.*&format=json").format(source_uri, sys_name, tray_name, slot_name)).json()
            for metric in metrics_list["results"]:
                metric_name = metric[slot_prefix :]
                metric_data = session.get(("{}/render?target=storage.eseries.{}.drive_statistics.{}.{}.{}&from=19700101&format=json&noNullPoints").format(source_uri, sys_name, tray_name, slot_name, metric_name)).json()
                for point in metric_data[0]["datapoints"]:
                    if point[0] is None:
                        continue
                    point_val = float(point[0])
                    point_timestamp = int(point[1])
                    point_item = dict(
                        measurement = "disks",
                        tags = dict(
                            sys_id = sys_id,
                            sys_name = sys_name,
                            sys_tray = tray_number,
                            sys_tray_slot = slot_number
                        ),
                        fields = dict(
                            {(metric_name, point_val)}
                        ),
                        time = datetime.utcfromtimestamp(point_timestamp).isoformat()
                    )
                    influxdb_payload.append(point_item)
    client.write_points(influxdb_payload, database=INFLUXDB_DATABASE)

def migrate_volume_metrics(sys_name, sys_id, source_uri):
    volume_stats_prefix = BASE_PREFIX + len(sys_name + ".volume_statistics.")

    session = requests.Session()
    session.auth = GRAFANA_AUTH
    client = InfluxDBClient(host=CMD.hostname, port=INFLUXDB_PORT, database=INFLUXDB_DATABASE,
                            username="admin", password="")
    influxdb_payload = list()

    # Query Web Services for storage system volumes
    # so we can get their ID for metric migration
    ws_session = get_proxy_session()
    name_id_pairs = list()
    ws_vol_list = session.get("http://{}:8080/devmgr/v2/storage-systems/{}/volumes".format(CMD.hostname,
                                                                                           sys_id)).json()
    for ws_vol in ws_vol_list:
        name_id_pairs.append((ws_vol["label"], ws_vol["id"]))

    volumes_list = session.get(("{}/metrics/expand?query=storage.eseries.{}.volume_statistics.*&format=json").format(source_uri, sys_name)).json()
    for volume in volumes_list["results"]:
        volume_name = volume[volume_stats_prefix :]
        volume_id = "null"
        for pair in name_id_pairs:
            if volume_name == pair[0]:
                volume_id = pair[1]
                break
        volume_prefix = volume_stats_prefix + len(volume_name) + 1 # remove volume name and .
        metrics_list = session.get(("{}/metrics/expand?query=storage.eseries.{}.volume_statistics.{}.*&format=json").format(source_uri, sys_name, volume_name)).json()
        for metric in metrics_list["results"]:
            metric_name = metric[volume_prefix :]
            metric_data = session.get(("{}/render?target=storage.eseries.{}.volume_statistics.{}.{}&from=19700101&format=json&noNullPoints").format(source_uri, sys_name, volume_name, metric_name)).json()
            for point in metric_data[0]["datapoints"]:
                if point[0] is None:
                    continue
                point_val = float(point[0])
                point_timestamp = int(point[1])
                point_item = dict(
                    measurement = "volumes",
                    tags = dict(
                        sys_id = sys_id,
                        sys_name = sys_name,
                        vol_id = volume_id,
                        vol_name = volume_name
                    ),
                    fields = dict(
                        {(metric_name, point_val)}
                    ),
                    time = datetime.utcfromtimestamp(point_timestamp).isoformat()
                )
                influxdb_payload.append(point_item)
    client.write_points(influxdb_payload, database=INFLUXDB_DATABASE)

def migrate_storage_system(sys_name, sys_id, source_uri):
    LOG.info(("    Disk metrics for \"{}\"...").format(sys_name))
    migrate_disk_metrics(sys_name, sys_id, source_uri)
    LOG.info(("    Volume metrics for \"{}\"...").format(sys_name))
    migrate_volume_metrics(sys_name, sys_id, source_uri)

def get_proxy_session():
    """
    Returns a session with the appropriate content type and login information.
    :return: Returns a request session for the SANtricity RestAPI Webserver
    """
    request_session = requests.Session()

    # Try to use what was passed in for username/password...
    username = CMD.proxyUsername
    password = CMD.proxyPassword
    
    if ((username is None or username == "") and (password is None or password == "")):
        username = "admin"
        password = "admin"

    request_session.auth = (username, password)
    # Ignore the self-signed certificate issues for https
    request_session.verify = False
    return request_session


##
# Main
##
if __name__ == "__main__":
    # Create our eseries database if it hasn't been already
    client = InfluxDBClient(host=CMD.hostname, port=INFLUXDB_PORT, database=INFLUXDB_DATABASE,
                            username="admin", password="")
    client.create_database(INFLUXDB_DATABASE)

    # Create a requests session to get our datasources from Grafana
    sources_uri = ("{}/api/datasources").format(QUERY_BASE_URL)
    session = requests.Session()
    session.auth = GRAFANA_AUTH
    req = session.get(sources_uri)

    executor = concurrent.futures.ProcessPoolExecutor(10)

    # Query Web Services for storage systems
    # so we can get their ID for metric migration
    ws_session = get_proxy_session()
    name_id_pairs = list()
    storage_system_list = session.get("http://{}:8080/devmgr/v2/storage-systems/".format(CMD.hostname)).json()
    for system in storage_system_list:
        name_id_pairs.append((system["name"], system["id"]))

    # We need to loop through all the datasources we received and find which ones
    # use Graphite. Then we can begin our queries and do the migration
    source_num = 0
    for item in req.json():
        if item["type"] != "graphite":
            continue
        LOG.info(("Found Graphite datasource #{}").format(source_num + 1))
        
        # We found a Graphite datasource, so let's migrate it
        source_id = item["id"]
        source_uri = ("{}/proxy/{}").format(sources_uri, source_id)

        # Get the list of storage systems in the database
        sys_list = session.get(("{}/metrics/expand?query=storage.eseries.*&format=json").format(source_uri)).json()
        LOG.info(("  Found {} storage systems, beginning migration").format(len(sys_list["results"])))
        migrator = list()
        for system in sys_list["results"]:
            sys_name = system[BASE_PREFIX : ]
            sys_id = "null"
            for pair in name_id_pairs:
                if sys_name == pair[0]:
                    sys_id = pair[1];
                    break
            migrator.append(executor.submit(migrate_storage_system, sys_name, sys_id, source_uri))
        concurrent.futures.wait(migrator)
        LOG.info("  Done!")

        source_num += 1
        
    LOG.info(("Finished migration of {} Graphite datasource{}").format(source_num, ("s" if source_num > 1 else "")))

