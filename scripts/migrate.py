#!/usr/bin/python
"""
Running this script will migrate performance metrics from a previous
Graphite Performance Analyzer database to the new InfluxDB database.
This is accomplished by querying the running Graphite database for 
collected metrics and generating new queries to push them to InfluxDB.
"""
import logging
import requests
import argparse
import json

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
PARSER.add_argument("-u", "--username", default="admin",
                    help="The username used to login to Grafana")
PARSER.add_argument("-p", "--password", default="admin",
                    help="The password used to login to Grafana")
CMD = PARSER.parse_args()

QUERY_BASE_URL = ("http://{}:3000").format(CMD.hostname)
GRAFANA_AUTH = (CMD.username, CMD.password)

##
# Metrics
##
DRIVE_PARAMS = [
    "averageReadOpSize",
    "averageWriteOpSize",
    "combinedIOps",
    "combinedResponseTime",
    "combinedThroughput",
    "otherIOps",
    "readIOps",
    "readOps",
    "readPhysicalIOps",
    "readResponseTime",
    "readThroughput",
    "writeIOps",
    "writeOps",
    "writePhysicalIOps",
    "writeResponseTime",
    "writeThroughput"
]

VOLUME_PARAMS = [
    "averageReadOpSize",
    "averageWriteOpSize",
    "combinedIOps",
    "combinedResponseTime",
    "combinedThroughput",
    "flashCacheHitPct",
    "flashCacheReadHitBytes",
    "flashCacheReadHitOps",
    "flashCacheReadResponseTime",
    "flashCacheReadThroughput",
    "otherIOps",
    "queueDepthMax",
    "queueDepthTotal",
    "readCacheUtilization",
    "readHitBytes",
    "readHitOps",
    "readIOps",
    "readOps",
    "readPhysicalIOps",
    "readResponseTime",
    "readThroughput",
    "writeCacheUtilization",
    "writeHitBytes",
    "writeHitOps",
    "writeIOps",
    "writeOps",
    "writePhysicalIOps",
    "writeResponseTime",
    "writeThroughput"
]


##
# Logging
##
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
requests.packages.urllib3.disable_warnings()
LOG = logging.getLogger("db_migrator")

##
# Migration functions
##

def migrate_disk_metrics(sys_name, client, base_prefix):
    trays_list = session.get(("{}/metrics/expand?query=storage.eseries.{}.drive_statistics.*&format=json").format(source_uri, sys_name)).json()
    for tray in trays_list["results"]:
        tray_name = tray[base_prefix :]
        tray_number = tray_name[5 :]
        tray_prefix = base_prefix + len(tray_name) + 1 # remove tray name and .
        slots_list = session.get(("{}/metrics/expand?query=storage.eseries.{}.drive_statistics.{}.*&format=json").format(source_uri, sys_name, tray_name)).json()
        for slot in slots_list["results"]:
            slot_name = slot[tray_prefix :]
            slot_number = slot_name[5 :]
            slot_prefix = tray_prefix + len(slot_name) + 1
            metrics_list = session.get(("{}/metrics/expand?query=storage.eseries.{}.drive_statistics.{}.{}.*&format=json").format(source_uri, sys_name, tray_name, slot_name)).json()
            for metric in metrics_list["results"]:
                influxdb_payload = list()
                metric_name = metric[slot_prefix :]
                metric_data = session.get(("{}/render?target=storage.eseries.{}.drive_statistics.{}.{}.{}&format=json").format(source_uri, sys_name, tray_name, slot_name, metric_name)).json()
                for point in metric_data[0]["datapoints"]:
                    if point[0] is None:
                        continue
                    point_val = float(point[0])
                    point_timestamp = int(point[1])
                    point_item = dict(
                        measurement = "disks",
                        tags = dict(
                            sys_id = 0, # TODO
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

def migrate_volume_metrics(sys_name, client, base_prefix):
    volumes_list = session.get(("{}/metrics/expand?query=storage.eseries.{}.volume_statistics.*&format=json").format(source_uri, sys_name)).json()
    for volume in volumes_list["results"]:
        volume_name = volume[base_prefix :]
        volume_prefix = base_prefix + len(volume_name) + 1 # remove volume name and .
        metrics_list = session.get(("{}/metrics/expand?query=storage.eseries.{}.volume_statistics.{}.*&format=json").format(source_uri, sys_name, volume_name)).json()
        for metric in metrics_list["results"]:
            influxdb_payload = list()
            metric_name = metric[volume_prefix :]
            metric_data = session.get(("{}/render?target=storage.eseries.{}.volume_statistics.{}.{}&format=json").format(source_uri, sys_name, volume_name, metric_name)).json()
            for point in metric_data[0]["datapoints"]:
                if point[0] is None:
                    continue
                point_val = float(point[0])
                point_timestamp = int(point[1])
                point_item = dict(
                    measurement = "volumes",
                    tags = dict(
                        sys_id = 0, # TODO
                        sys_name = sys_name,
                        vol_id = 0, # TODO
                        vol_name = volume_name
                    ),
                    fields = dict(
                        {(metric_name, point_val)}
                    ),
                    time = datetime.utcfromtimestamp(point_timestamp).isoformat()
                )
                influxdb_payload.append(point_item)
            client.write_points(influxdb_payload, database=INFLUXDB_DATABASE)

def migrate_storage_system(sys_path, client):
    base_prefix = len("storage.eseries.")    
    sys_name = sys_path[base_prefix :]
    LOG.info(("Found system \"{}\"").format(sys_name))
    LOG.info("  Migrating...")
    LOG.info("    Disk metrics...")
    migrate_disk_metrics(sys_name, client, base_prefix + len(sys_name + ".drive_statistics."))
    LOG.info("    Volume metrics...")
    migrate_volume_metrics(sys_name, client, base_prefix + len(sys_name + ".volume_statistics."))

##
# Main
##
if __name__ == "__main__":
    client = InfluxDBClient(host=CMD.hostname, port=INFLUXDB_PORT, database=INFLUXDB_DATABASE,
                            username="admin", password="")

    # create our eseries database if it hasn't been already
    client.create_database(INFLUXDB_DATABASE)

    sources_uri = ("{}/api/datasources").format(QUERY_BASE_URL)
    session = requests.Session()
    session.auth = GRAFANA_AUTH

    req = session.get(sources_uri)

    # We need to loop through all the datasources we received and find which ones
    # use Graphite. Then we can begin our queries and do the migration
    source_num = 1
    for item in req.json():
        if item["type"] != "graphite":
            continue
        LOG.info(("Found Graphite datasource #{}").format(source_num))
        
        # We found a Graphite datasource, so let's migrate it
        source_id = item["id"]
        source_uri = ("{}/proxy/{}").format(sources_uri, source_id)

        # Get the list of storage systems in the database
        sys_list = session.get(("{}/metrics/expand?query=storage.eseries.*&format=json").format(source_uri)).json()
        for system in sys_list["results"]:
            migrate_storage_system(system, client)

        source_num += 1


