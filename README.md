# Punch Demos

> This repo embeds all the ressources needed to execute some uses cases from end to end.

## Uses cases:
> The following list describes the final uses cases provided by this repo.

1) Airspace Monitoring : Airspace
2) Application Usage Monitoring : Usage
3) Aircraft Predictive Maintenance : Aircraft

### 1) Airspace Monitoring
![alt text](resources/airspace.gif)
### 2) Application Usage Monitoring
![alt text](resources/usage.gif)
### 3) Aircraft Predictive Maintenance
![alt text](resources/aircraft_maintenance_predictive.gif)

## Repo Structure :
```
├── conf
├── generators
├── data
├── README.md
└── resources
```
- conf : Punch conf dir
- generators : Dataset generator
- data : Some mandatory data used by dashboards (ex : world-map)
- resources : Documentation additionnal resources

## How to deploy?

### Requirements :

- Install a fresh Punch standalone >=6.1
- Download a filebeat
- git clone this repo
- Start your punch standalone

- export PUNCH_DEMO_DIR=<Path_to_your_demo_dir>
- export PUNCHPLATFORM_CONF_DIR=<path_to_your_punch_conf_repo>
- export PUNCHPLATFORM_BINARIES_DIR=$PUNCHPLATFORM_CONF_DIR/../external/punch-binaries-<version>

### Run :
> $PUNCH_DEMO_DIR/run.sh needs rights to create /data repo

- $PUNCH_DEMO_DIR/.run.sh
- <Path_to_your_filebeat>/filebeat -e -c $PUNCH_DEMO_DIR/conf/filebeat.yml
- channelctl -t <tenant> start
