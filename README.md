# NetApp E-Series Grafana Performance Dashboards

This project incorporates several different Open Source components in order to simply and beautifully demonstrate the
performance of one or more E-Series systems at different levels/layers. It is intended to serve as a reference implementation
for the use of Grafana to visualize the performance of your E-Series systems. It is also intended to be customizable and
extensible based on your individual needs.


## Overview
In a nutshell, the Web Services Proxy will periodically poll your storage-system[s] for performance data, which we will collect
 at a regular and consistent interval using a simple Python script. This script will push the data into a Graphite database,
 which is a database for storing metrics data. Grafana, a data visualization engine for time-series data, is then utilized
 along with several customized dashboards to present the data graphically. All of these components are integrated together by
 using Docker and Ansible.

The only real requirements to utilize this project are a Linux OS and a Docker installation. ~95% of the installation and
configuration process is automated using Ansible and Docker.

Our descriptions below of the aforementioned components will in no way fully do them justice. It is recommended that you visit
the project/home pages for each in order to gain a full understanding of what they can provide and how they can be fully
utilized. We will attempt to provide the information that you absolutely need to know, but probably little beyond that.

## Components
### Graphite
[Graphite](https://graphiteapp.org/) acts as our persistent store for preserving metrics data. There are many [different
back-ends](https://grafana.com/plugins?type=datasource) that can be utilized with Grafana for storing metrics, but we chose
Graphite due to its simplicity and the storage efficiency that it can provide. Graphite not only allows a variety of flexible
queries to be utilized for summarizing the stored metrics, but it also allows data points to be summarized and granularity to
be reduced over time to reduce disk utilization.

There are many users of Graphite that use it to preserve **years** worth of behavioral data metrics for their applications.

While we do have a Python script predefined for use with Graphite and the Web Services Proxy for collecting E-Series
performance metrics, we have also provided some additional collector example scripts at the root of the project, one in Python,
 the other in Bash. If you would like to provide additional metrics to Graphite, you may used these as a starting sample. If
 you do need to troubleshoot the metrics collection in Graphite, there are also logs available within the Graphite container
 that will show metrics that are being pushed. `docker exec -it graphite tail -f /var/log/carbon.log`

### Grafana
[Grafana](https://grafana.com/) is an open-source tool designed to help you visualize time-series data. It has the capability
to accept plug-ins for additional functionality, but its core provides a lot of power with no add-ons.

Data from a configure datasource is displayed in Grafana via user-defined dashboards. Grafana dashboards are
built/generated in the GUI, but are stored/represented in JSON format on disk. While we provide several pre-built dashboards,
it is entirely possible (and encouraged), for you to [create your own](http://docs.grafana.org/guides/getting_started/) in
Grafana. The pre-built dashboards are available in: ** *&lt;install_dir&gt;/ansible/dashboards/* **

### NetApp SANtricity Web Services Proxy
The Web Services Proxy, provides a RESTful interface for managing/monitoring E-Series storage systems. Our newest hardware
 models provide a RESTful API out-of-the-box, but the Web Services Proxy will support the newest systems as well as the legacy
 storage systems that do not. It is highly scalable and can support upwards of 500 E-Series systems while using < 2 GB of
 memory.

 The Web Services Proxy is provided with the default configuration and settings,
  and it may be accessed at *yourhost:8080*. If you do not wish for the API to be made accessible externally, you may remove
  the port mapping in the docker-compose.yml file.

  ~~~~
netapp_web_services:
    ...
    ports:
      - 8080:8080
      - 8443:8443
  ~~~~

  The Web Services Proxy installation includes a GUI component that can be utilized to manage the newest E-Series systems (systems running
  firmware levels 11.40 and above), which may or may not work for your environment.

  By default we will utilize default credentials for accessing the Web Services Proxy (*admin/admin*). These credentials may be updated, but
  you will need to update the credentials file for the collector script when doing so (** *&lt;install_dir&gt;/collector/config.json* **). These credentials can optionally be passed as arguments to the collector script (*-u USERNAME -p PASSWORD*) which will cause the *config.json* credentials to be ignored. Environment variables for this purpose are exposed in the docker-compose.yml file's stats_collector section.

## Supporting Tools
Installing each of these components and configuring them properly on an arbitrary OS version can be difficult. Rather than
requiring a complex installation and configuration step, we utilize a couple of different tools to facilitate the deployment.

### Ansible
We use [Ansible](https://www.ansible.com/) in order to define/apply a consistent configuration for the different components
listed above. A simple Ansible Playbook can save thousands of lines worth of shell scripting.

Primarily, we utilize Ansible to configure Grafana and import/export the dashboards as required.

### Docker
[Docker](https://www.docker.com/) allows you to define an environment to run a particular application in code, including the
OS, dependencies, and any required configuration/customization. It is similar to creating a custom virtual machine image for
each component, but much easier, more dynamic, and lighter weight resource-wise. Such a configuration is known as a Docker
image. Each component either has an Official, Unofficial, or custom-built Docker image that defines the environment
and configuration such that only installation of Docker is required to utilize it.

[Docker-Compose](https://docs.docker.com/compose/) allows multiple Docker images to be orchestrated together to solve a larger
problem. A common example is a Web Server that also requires a Database.

In our case, we have several components that must be run together for everything to work correctly, there are startup
dependencies, and certain components require communication with other components. Docker-Compose allows us to define the
various services we require, how they should behave, where they should store their data, and which should be externally
accessible, all via the docker-compose.yml file.

## Getting Started
### Dependencies
You'll need to install [Docker](https://docs.docker.com/install/) and [Docker-Compose](https://docs.docker.com/compose/install/).
 Virtually all of the other dependencies are provided through other Docker images.

### Configuration

#### Managed Systems

#### Dashboards
The dashboards are located in ** *&lt;install_dir&gt;*/ansible/dashboards/ ** and will be imported into Grafana when started.
 Dashboards can also be imported from within the Grafana interface by navigating to **Dashboards->Home**, clicking on the
 drop-down at the top of the page, and selecting **Import Dashboard**.

Dashboards are imported/exported using JSON and that documentation can be found [here](http://docs.grafana
.org/reference/dashboard/). You may use the provided pre-configured dashboards as a reference for creating your own.

We have provided an export script ** *&lt;install_dir&gt;*/backup.sh ** for automatically exporting new / user-modified dashboards to disk for backup. This pulls current dashboards from the service and stores them locally in the ** *&lt;install_dir&gt;*/ansible/dashboards/backup ** directory in JSON format. The Grafana service must be running when you execute this script.

#### Storage Arrays
Arrays to be monitored are located in ** *&lt;install_dir&gt;*/ansible/arrays/ ** and will be automatically added to the Web Services Proxy
when the services start. These are currently represented with JSON files, in which you provide the IP address[es] and a
unique ID for each storage-system that you wish to manage. This is intended to be a simplified workflow. Each set of arrays should preferably be added to their own JSON file with a unique ID and their IPs represented as a comma separated list with additional parameters like so:
```json
{
  "id": "string",
  "controllerAddresses": [
    "string",
    "string",
    "string"
  ],
  "acceptCertificate": false,
  "validate": false,
  "password": "string",
  "wwn": "string",
  "enableTrace": true,
  "metaTags": [
    {
      "key": "string",
      "valueList": [
        "string"
      ]
    }
  ]
}
```
Please note that if the JSON is formatted improperly this step will fail and notify you. Also be aware that the ID *must be unique* or the add will fail because that system already exists. You can omit the ID line from the JSON file and a valid unique ID will be generated for you. Here is an example of what a simple array JSON file might look like:
```json
{
  "controllerAddresses": [
    "10.1.1.1",
    "10.1.2.3",
    "10.3.4.5",
  ],
  "acceptCertificate": true,
  "validate": true,
  "password": "myPass",
  "metaTags": [
    {
      "key": "myTag",
      "valueList": [
        "value1", 
        "value2"
      ]
    }
  ]
}
```
It is also possible to
 manually add storage-systems using the Web Services Proxy interactive API documentation found at **yourhost:8080/devmgr/docs/#/Storage-Systems/new_StorageSystem**.

Once everything is started, arrays can also be managed through the SANtricity® Unified Manager as described below. Note that
although they will still be monitored, legacy arrays added through the API/config files will not appear in this manager.

#### Graphite and Carbon
Graphite's method and frequency of storing metrics is configurable through config files in the ** *&lt;install_dir&gt;*/graphite **
 directory. There are two different config files to look at here.

##### carbon.conf
This file is used to configure where and how Carbon collects metrics. The documentation for each setting is written in the comments in the file itself.

##### storage-schemas.conf
This file is responsible for defining retention rates for metric storage. The retention rates defined here for each section must all be multiples of each other. For example: 5s, 15s, 30s, 60s. Detailed documentation for this file can be found [here](https://graphite.readthedocs.io/en/latest/config-carbon.html#storage-schemas-conf).

Note that changes made to retention rates will invalidate data collected before the changes were made.

### Starting It Up
It's pretty simple: run the start.sh script. This will begin the process of building, setting up, and running everything. When you want to stop it, run the stop.sh script. If you're trying to monitor the status of any of these tools, you can do so using standard Docker commands. To remove any current container instances, run the clean.sh script after stopping.

Once everything is started, you have access to several pages to control and configure.

#### Accessing the Web Services Proxy
The Web Services Proxy can be accessed at **yourhost:8080**. From here you can access the SANtricity® Unified Manager (default credentials *admin/admin*) which is a UI front-end for managing storage arrays. There are also links to the Web Services API reference as well as the NetApp support site.

#### Accessing the Grafana Interface and Dashboards
The dashboards are available at **yourhost:3000** with default credentials of *admin/admin*. Grafana should be pre-configured for immediate access to your data. There are also dashboards for displaying data related to Graphite's Carbon component, which is the component responsible for collecting and writing metric data to disk.

Documentation for additional configuration and navigation can be found [here](http://docs.grafana.org/guides/getting_started/).
