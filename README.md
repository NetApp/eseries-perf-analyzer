# NetApp E-Series Grafana Integration

Welcome! This package incorporates several different tools in order to provide an easy to use interface to the Web Services Proxy. Its purpose is to collect exposed metrics on our storage arrays via APIs. This data can then be visualized through the highly customizable Grafana front-end.

This out-of-the-box solution is designed to require minimal additional configuration for getting things up and running and begin seeing the data you want to see.

## Overview
Capturing time-series data in a way that is manageable and scalable isn't an easy task. We use several different open-source tools in order to do so very simply.

From the top-level, data is presented from Grafana via JSON-defined dashboards. We provide several pre-configured dashboards, but it's possible to define your own. The data that powers these dashboards is provided via the Graphite back-end. We push data into Graphite using Python code. These tools are given a standard environment to work in using Ansible. Finally, we use Docker to put all of these tools into a deployable package for simplicity and portability.

## Components
### Graphite
[Graphite](https://graphiteapp.org/) is a monitoring tool that provides our persistent store for preserving metrics data. The back-end can be configured to expire metrics data over time, as well as analyze/summarize data using a variety of strategies in order to allow long periods of historical data to be preserved without using too much disk space.

There are many users of Graphite that use it to preserve **years** worth of performance data for their application.

There are example collector scripts at the root of the project, one in Python and the other in Bash. You can use these to see how metrics can be provided to Graphite. There are also logs available within the Graphite container (*@/var/log/carbon.log*) to help troubleshoot any issues with a collector.

### Grafana
[Grafana](https://grafana.com/) is an open-source tool designed to help you visualize time-series data. It is incredibly customizable and can be used to view data from a variety of data stores all from a familiar and easy to use web-based UI.

The data stored in Graphite is displayed in Grafana via user-defined dashboards. Grafana dashboards are represented in JSON. Many of these dashboards can be configured directly from the Grafana UI to tune for the exact data you want to see. We provide pre-defined examples and they can be found in ** *install_dir*/ansible/dashboards/ **


## Supporting Tools
As you can see, we use a variety of components in order to provide all of this functionality. Due to the difficulty of installing individual components on a given server, we use a few supporting tools in order to make the process easier.

### Ansible
We use [Ansible](https://www.ansible.com/) in order to define a consistent environment for the different components listed above. A simple Playbook saves thousands of lines worth of shell scripting.

### Docker
We use [Docker](https://www.docker.com/) and [Docker-Compose](https://docs.docker.com/compose/) for our deployment method because of the simplicity that it provides even when deploying many separate components.

## Getting Started
### Dependencies
You'll need to install [Docker](https://docs.docker.com/install/) and [Docker-Compose](https://docs.docker.com/compose/install/). Most of the other dependencies are provided via individual Docker images.

This also assumes you already have managed storage arrays ready to be monitored. More information on this can be found below.

### Configuration
*//TODO Define a template to allow a new configuration to be generated using a given server hostname and port.*

##### Dashboards
The dashboards are located in ** *install_dir*/ansible/dashboards/ ** and will be imported into Grafana when started. Dashboards can also be imported from within the Grafana interface by navigating to **Dashboards->Home**, clicking on the dropdown at the top of the page, and selecting **Import Dashboard**.

Dashboards are represented using JSON and that documentation can be found [here](http://docs.grafana.org/reference/dashboard/).

##### Storage Arrays
Arrays to be monitored are located in ** *install_dir*/ansible/arrays/ ** and will be managed automatically when everything is started. These are currently represented as JSON files, and each array must be assigned a unique ID.

Once everything is started, arrays can also be managed through the SANtricity® Unified Manager as described below. Note that older/legacy arrays added through the API/config files will not appear in this manager.


### Starting It Up
It's pretty simple: run the start.sh script. This will begin the process of building, setting up, and running everything. When you want to stop it, run the stop.sh script. If you're trying to monitor the status of any of these tools, you can do so using standard Docker commands. To remove any current container instances, run the clean.sh script after stopping.

Once everything is started, you have access to several pages to control and configure.

#### Accessing the Web Services Proxy
The Web Services Proxy can be accessed at **yourhost:8080**. From here you can access the SANtricity® Unified Manager (default credentials *admin/admin*) which is a UI front-end for managing storage arrays. There are also links to the Web Services API reference as well as the NetApp support site.

#### Accessing the Grafana Interface and Dashboards
The dashboards are available at **yourhost:3000** with default credentials of *admin/admin*. Grafana should be pre-configured for immediate access to your data. Documentation for additional configuration and navigation can be found [here](http://docs.grafana.org/guides/getting_started/).

By running the backup.sh script it will backup current dashboards into ** *install_dir*/ansible/dashboards/backup **
