
# Super Simple Monitoring

Welcome! This tool is designed and intended to give you a deeper view into the inner workings of the Web Services Proxy. We expose various metrics via API's and via Java Management eXtensions (JMX), that this tool is capable of collecting and helping you visualize through the highly customizable Grafana front-end.

## Components
Capturing time-series data in a way that is manageable and scalable isn't an easy task. We use several different open-source tools in order to do so very simply.

From the top-level, data is presented from Grafana via defined dashboards. We provide several pre-configured dashboards, but
it's possible to define your own. The data that powers these dashboards is provided via the Graphite back-end. We push data
into Graphite primarily using Python code, but we also use jmxtrans, as shown below.

### JMX / jmxtrans

We expose Java [MBeans](https://docs.oracle.com/javase/tutorial/jmx/mbeans/index.html) in Web Services that provide information on the inner workings of the API. The Java Virtual Machine (JVM), exposes many of its own metrics that are also very usable.

While the JDK comes with some simple UI's to allow this data to be captured, they don't preserve historical data. [jmxtrans](https://github.com/jmxtrans/jmxtrans) is a project that serves as a bridge between the JVM and the logging/capture software that can make use of the metrics. It is capable of capturing JMX metrics from multiple JVM's and sending them to a a variety of mediums, including Graphite, which is what we use.

### Graphite
[Graphite](https://graphiteapp.org/) is a monitoring tool that provides our persistent store for preserving metrics data. The back-end can be configured to expire metrics data over time, as well as analyze/summarize data using a variety of strategies in order to allow long periods of historical data to be preserved without using too much disk space.

There are many users of Graphite that use it to preserve **years** worth of performance data for their application.

There are example collector scripts at the root of the project. You may use these to see how metrics can be provided to
Graphite. There are also logs available within the Graphite container (@ /var/log/carbon.log) available to help troubleshoot
any issues with a collector.

### Grafana
[Grafana](https://grafana.com/) is an open-source tool designed to help you visualize time-series data. It is incredibly customizable and can be used to view data from a variety of data stores.


## Supporting Tools
As you can see, we use a variety of components in order to provide this functionality. Due to the difficulty of installing individual components on a given server, we use a few supporting tools in order to make the process easier.

### Ansible
We use Ansible in order to define a consistent environment for the different components listed above. A simple Playbook saves thousands of lines worth of shell scripting.

### Docker
We use Docker and Docker-Compose for our deployment method because of the simplicity that it provides even when deploying many separate components.

## Getting Started
### Dependencies
You'll need [Docker](https://docs.docker.com/install/) and Docker-Compose installed. Most of the other dependencies are provided via individual Docker images.

### Configuration
By default, the configuration is setup to allow the local machine to be monitored on port 8099. The Web Services Proxy is configured to allow this in <install_dir>/webserver.sh under debug_options, but it is disabled by default. Enabling this option will allow the JMX statistics to be captured.
//TODO Define a template to allow a new configuration to be generated using a given server hostname and port.

#### Configuring Targets
The jmxtrans-targets/config.json file contains the configuration for pulling metrics from a single JVM instance. It is possible to have multiple files in the directory in order to poll multiple instances. By default, we will attempt to poll from an instance running on the localhost with a port of 8099.
There is a DEBUG_OPTIONS property in the webserver.sh file of the Web Services Proxy install directory that will enable remote JMX capabilities.

### Starting It Up
It's pretty simple, run the start.sh script. When you want to stop it, run the stop.sh script. If you're trying to monitor status, you can do so using standard Docker commands.

### Accessing the Dashboards
The dashboards are available at yourhost:3000, with default credentials of admin/admin.
