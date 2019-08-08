# NetApp E-Series Performance Analyzer
This project provides an automated installation and deployment of the NetApp E-Series Performance Analyzer, a collection of software and scripts for monitoring the performance of NetApp E-Series storage systems.

This project is intended to allow you to quickly and simply deploy an instance of our performance analyzer for monitoring your E-Series storage systems. We incorporate various open source components and tools in order to do so. While it is primarily intended to serve as a reference implementation for using Grafana to visualize the performance of your E-Series systems, it is also intended to be customizable and extensible based on your individual needs.

## Quickstart Guide
You'll need to have [Docker (v1.13.0+)](https://docs.docker.com/install/) and [Docker-Compose](https://docs.docker.com/compose/install/) installed in order to get started. We also utilize [Make](https://www.gnu.org/software/make/) for starting/stopping the components so make sure you have a version of that installed.

The storage systems to be monitored must be defined in the *"<project_dir\>/collector/config.json"* file. There is an example file located at *"<project_dir\>/collector/config.sample.json"* for your reference. You may also choose to add the systems to Web Services manually, as detailed below.

Once Docker is installed and the storage systems are configured, run the command _"make run"_ in the project's root folder. You will then be prompted for confirmation to download the necessary container images. If you wish to update to a newer image tag, you can cancel out and do so now. Within a few minutes, all dependencies should be retrieved and installed, and the performance analyzer should be running.

Open **http://<host\>:3000/d/ZOshR4NZk/system-view-dashboard** to reach the Grafana login page and the E-Series System View dashboard. Use the default login credentials of _admin/admin_ for first-time login.

## Overview
The Web Services Proxy will periodically poll your storage system(s) for performance data at a regular interval. Using a simple Python script, this data is collected and pushed into an [InfluxDB](https://www.influxdata.com/) time-series database. [Grafana](https://grafana.com/), a data visualization engine for time-series data, is then utilized along with several customized dashboards to present the data graphically. All of these components are integrated together using [Docker](https://www.docker.com/) and [Ansible](https://www.ansible.com/).

The only real requirements to utilize this project are a Linux OS and a Docker installation. ~95% of the installation and configuration process is automated using Ansible and Docker.

Our descriptions below of the various components will in no way fully do them justice. It is recommended that you visit the project/home pages for each in order to gain a full understanding of what they can provide and how they can be fully utilized. We will attempt to provide the high-level information that you absolutely need to know, but probably little beyond that.

## Components
### NetApp SANtricity Web Services Proxy
The Web Services Proxy provides a RESTful interface for managing/monitoring E-Series storage systems. Our newest hardware models provide a RESTful API out-of-the-box, but the Web Services Proxy will support the newest systems as well as the legacy storage systems that do not. It is highly scalable and can support upwards of 500 E-Series systems while using < 2 GB of memory.

The Web Services Proxy is provided with the default configuration and settings. It can be accessed at **http://<host\>:8080**. If you do not wish for the API to be externally accessible, you may remove the port mapping in the _"docker-compose.yml"_ file in the root folder of the project:
~~~~
netapp_web_services:
    ...
    ports:
      - 8080:8080
      - 8443:8443
~~~~

The Web Services Proxy installation includes a GUI component that can be used to manage the newest E-Series systems (those running firmware levels 11.40 and above), which may or may not work for your environment.

By default we will use the credentials _admin/admin_ for accessing the Web Services Proxy. These credentials can be updated, but you will need to update the credentials in your storage system config file *"<project_dir\>/collector/config.json"* as well. These credentials can optionally be passed as arguments to the collector script (_"-u USERNAME -p PASSWORD"_) which will cause the _config.json_ credentials to be ignored. Environment variables for the purpose are exposed in the *"<project_dir\>/docker-compose.yml"* file's *stats_collector* section.
### InfluxDB
[InfluxDB](https://www.influxdata.com/) is our persistent store for preserving metrics data. Grafana supports [many different backends](https://grafana.com/plugins?type=datasource), but we chose InfluxDB due to its speed and scalability as well as the power and simplicity of its query language.

While we do have a Python script predefined for use with InfluxDB and the Web Services Proxy, which collects E-Series performance metrics, we also provide some additional collector example scripts at the root of the project. One of these is written in Python, and the other in Bash. If you would like to provide additional metrics for collection, you may use these scripts as an example.
### Grafana
[Grafana](https://grafana.com/) is an open-source tool designed to help you visualize time-series data. It has the capability to accept plugins for additional functionality, but its core provides a lot of power with no addons.

Data from a configured datasource is displayed in Grafana via user-defined dashboards. Grafana dashboards are built/generated in the GUI, but are stored/represented in JSON format on disk. While we provide several pre-built dashboards, it is entirely possible (and encouraged) for you to [create your own](http://docs.grafana.org/guides/getting_started/). The source for our dashboards can be found in *"<project_dir\>/ansible/dashboards/"*.

## Supporting Tools
Installing each of these components and configuring them properly on an arbitrary OS version can be difficult. Rather than requiring a complex installation and configuration step, we utilize a couple of different tools to facilitate this type of deployment.
### Ansible
We use [Ansible](https://www.ansible.com/) in order to define and apply consistent configurations for the different components listed above. A simple Ansible playbook can save thousands of lines worth of shell scripting.

Primarily, we utilize Ansible to configure Grafana and import/export dashboards as required.
### Docker
[Docker](https://www.docker.com/) allows you to define an environment to run a particular application in code, including the OS, dependencies, and any required configuration/customization. It is similar to creating a custom virtual machine image for each component, but much easier, more dynamic, and lighter weight resource-wise. Such a configuration is known as a Docker image. Each component of our solution has an official, unofficial, or custom-built Docker image that defines its environment and configuration such that only an installation of Docker is required to use it.

We use version 2 of the Compose file format, with features that require at least Docker version 1.13.0+.

[Docker-Compose](https://docs.docker.com/compose/) allows multiple Docker images to be orchestrated together to solve a larger problem. A common example is a web server that also requires a database.

In our case, we have several components that must be run together for everything to work correctly. There are startup dependencies, and certain components require communication with other components. Docker-Compose allows us to define the various services we require, how they should behave, where they should store their data, and which should be externally accessible. This is all done via the *"<project_dir\>/docker-compose.yml"* file.

## Getting Started
### Dependencies
You'll need to install [Docker](https://docs.docker.com/install/) and [Docker-Compose](https://docs.docker.com/compose/install/). All other dependencies are provided through use of our Docker images. You also need access to [Make](https://www.gnu.org/software/make/).
### Configuration
#### Storage Systems
Arrays to be monitored should be added to the *"<project_dir\>/collector/config.json"* file. A sample configuration file is provided at *"<project_dir\>/collector/config.sample.json"* for reference. For most systems, you will also need to provide a valid password to log in to the target storage system. If you do not, or you provide an incorrect password, it's possible that we won't be able to pull performance data for that system.

It is also possible to manually add storage systems using the Web Services Proxy interactive API documentation found at **http://<host\>:8080/devmgr/docs/#/Storage-Systems/new_StorageSystem**.

Once everything is started, arrays can also be managed through the SANtricity® Unified Manager as described below. Note that although they will still be monitored, legacy arrays added through the API/config files will not appear in this manager.
#### InfluxDB
InfluxDB is configurable through the config file located at *"<project_dir\>/influxdb/influxdb.conf"*. Information about configuration options can be found [here](https://docs.influxdata.com/influxdb/v1.7/administration/config/).
#### Dashboards
The dashboards are located in *"<project_dir\>/ansible/dashboards/"* and will be imported into Grafana when started. Dashboards can also be imported from within the Grafana interface by navigating to **Dashboards->Home**, clicking on the drop-down at the top of the page, and selecting **Import Dashboard**.

Dashboards are imported/exported using JSON and that documentation can be found [here](http://docs.grafana.org/reference/dashboard/). You may use the provided pre-configured dashboards as a reference for creating your own. We have provided a make target for automatically exporting new/user-modified dashboards to disk for backup. This pulls current dashboards from the service and stores them locally in the *"<project_dir\>/backups/"* directory in JSON format. To execute this simply run the command _"make backup-dashboards"_ in the root folder of the project. The Grafana instance must be running when you execute this command.
### Starting It Up
It's pretty simple: run the command _"make run"_ from within the project root directory. This will begin the process of building, setting up, and running everything. When you want to stop it, run the command _"make stop"_. If you're trying to monitor the status of any of these tools, you can do so using standard Docker commands. To remove any current container instances, run the command _"make clean"_. A list of all possible make targets can be viewed using the _"make help"_ command.

_"make run"_ will prompt you for confirmation on whether or not you wish to continue and allow the downloading of default container images. If you wish to update to a newer tag image, you can cancel out and do so now.

We've done our best to ensure that the configured Docker images not only build and work in most environments, but that they are also well-used and tested by the community, and don't have security holes. New security issues are found all of the time, however, and we may not be able to update the image tags immediately. You may choose to change the image tags to a newer or different version, just be aware that we haven't tested that variation and you might run into problems with the build or during runtime.

Once everything is started, you have access to several pages to control and configure.

## Once It's Started
### Accessing the Web Services Proxy
The Web Services Proxy can be accessed at **http://<host\>:8080**. From here you can access the SANtricity® Unified Manager using default credentials of _admin/admin_. This is a UI frontend for managing storage arrays. There are also links to the Web Services API reference as well as the NetApp support site.
### Accessing the Grafana Interface and Dashboards
The dashboards are available at **http://<host\>:3000** using default credentials _admin/admin_. Grafana should be pre-configured for immediate access to your data. Documentation for additional configuration and navigation can be found [here](http://docs.grafana.org/guides/getting_started/).
### Migrating data from a previous Performance Analyzer instance
If you have been using a previous version of the Performance Analyzer, your metric data was stored in a Graphite database. Newer versions of the Performance Analyzer rely on InfluxDB for its data backend. We have provided a method for migrating your previous data over to this new backend by following a few simple steps:
##### 1. Verify you have a graphite_database folder in the root of your project
This ensures that there is indeed data that needs migrating. If such a folder doesn't exist, there is no need for migration.
##### 2. Re-enable the Graphite backend
Because we no longer user Graphite as our data backend, the service is no longer required to be running. We have, however, left it available for the purposes of data migration. Open the *"<project_dir\>/docker-compose.yml"* file and find the commented-out section labeled graphite:
~~~~
#  graphite:
#    image: ${PROJ_NAME}/graphite:${TAG}
#    build:
#      context: ./graphite
#    container_name: graphite
#    depends_on:
#      - netapp_web_services
#    mem_limit: 2G
#    restart: unless-stopped
#    ports:
#      - 80
#      - 2003-2004
#      - 2023-2024
#      - 8125/udp
#      - 8126
#    logging:
#      driver: "json-file"
#      options:
#        max-file: "5"
#        max-size: 10m
#    volumes:
#      - ./graphite-database:/opt/graphite/storage/whisper
~~~~
Uncomment this block (remove all of the #s) and save the file. Open the *"<project_dir\>/ansible/main.yml"* file and uncomment this line (remove the #):
~~~~
#- include_tasks: tasks/graphite_datasource.yml
~~~~

Simply start everything up by running _"make run"_ (or _"make restart"_ if services are already running).
##### 3. Initiate data migration
Once it has started back up, you can initiate data migration by running the command _"make migrate-graphite"_. Once this is completed, and you have verified that your data correctly appears on your dashboards, you may recomment the blocks shown above and restart the services one final time.

## Troubleshooting
### I don't have access to Docker
At this time (and this is unlikely to change), Docker is a hard requirement for using this project.
### I don't have network access on this machine
Your only option at this point is to save/export the Docker images on a machine that does have general internet access and then copy them and import them to the target machine. This is an advanced workflow that we do not currently cover in this guide, but is not overly difficult to achieve.
### I can't pull the Docker images
Check your access to DockerHub. If you are running this on a machine with network segregation, you may need to update your Docker binary to utilize a local DockerHub mirror or repository to get this to work.
### A Docker image failed to build
We pin our Docker images to a known good tag at the time that we commit changes. The downside to pinning to a major/minor version rather than a specific image hash is that while you do get the benefit of new patches (security updates, etc.), the possibility of breakage does exist. If an image fails to build, try to determine where the failure occurred and if it's an environment issue or an issue with an update to the Docker image tag. It's quite likely that you'll be able to get things to function correctly by rolling back to an older version.
### I don't see any data in the charts
Did you remember to add any storage systems to the Web Services Proxy instance, either through the Ansible helper scripts or manually? If not, you didn't give us anything to push metrics on yet.

Assuming that you did, verify that the collector container is running and that it is successfully collecting metrics. You can do this by checking the container logs by running the command _"docker logs -f collector"_.

If you have added your own metrics that aren't showing up, verify that you're sending the data to the correct server address and port.
### I made some changes to <X\> and now everything is broken!
While we do encourage variations, improvements, and additions, these are definitely something we can't support. While you may enter an issue and/or ask for help, we can't guarantee that we can, or will try to fix your deployment and may ask you to revert to a known configuration.
### I get prompted each time I perform "make run"
You may add _"QUIET=1"_ to the *"<project_dir\>/deploy.env"* file. This will automatically choose "yes" when prompted by the build/run process.
