[Architecture](wma-architecture.pdf)

# wma-server
wmbus analytics server

Example config for wmbusmeters installation
- working for snap on server Ubuntu 24.04.1 LTS

# Installation using container
docker run -d --privileged \
    --name=wmbusmeters \
    --restart=always \
    -v /etc/localtime:/etc/localtime:ro \
    -v /opt/wmbusmeters:/wmbusmeters_data \
    -v /dev/:/dev/ \
    wmbusmeters/wmbusmeters
## or without privilege
docker run -d \
    --name=wmbusmetersdirect \
    --restart=always \
    -v /etc/localtime:/etc/localtime:ro \
    -v /opt/wmbusmeters:/wmbusmeters_data \
    --device=/dev/ttyACM0 \
    wmbusmeters/wmbusmeters

--> folders are mounted to hosts /opt/wmbusmeters
--> generates log data from devices in /opt/wmbusmeters/logs


##### Setup MQTT on HOST:
(- sudo apt install mosquitto mosquitto-clients)
- add to /etc/mosquitto/mosquitto.conf
  - listener 1883
  - allow_anonymous true
- sudo systemctl restart mosquitto
- get Host IP 
  - hostname -I | awk '{print $1}'
- (test) pub in container:
  - mosquitto_pub -h <host-ip> -t "test/topic" -m "Hello MQTT"
    - e.g. mosquitto_pub -h 192.168.176.147 -t "test/topic" -m "Hello MQTT"

##### conf:
```
loglevel=normal
device=auto:t1
#device=/dev/ttyACM0:usb-IMST_iU891A-if00:t1
#device=/dev/ttyAMA0:iu891a:c1,t1
#device=iu891a:c1,t1
#device=iu891a:t1
#device=/dev/ttyACM0:iu891a:t1
#device=iu891a[00202071]:t1
#device=/dev/ttyACM0:t1
#device=/dev/ttyUSB0:iu891a:c1,t1
#device=iu891a[00202071]:t1
donotprobe=/dev/ttyAMA0
#donotprobe=all
logtelegrams=true
format=json
meterfiles=/wmbusmeters_data/logs/meter_readings
meterfilesaction=overwrite
logfile=/wmbusmeters_data/logs/wmbusmeters.log
shell=/usr/bin/mosquitto_pub -h 192.168.176.147 -t wmbusmeters/$METER_ID -m "$METER_JSON"
#shell=psql water -c "insert into consumption values ('',,'') "
# The alarmshell is executed when a problem with the receiving radio hardware is detected.
#alarmshell=/usr/bin/mosquitto_pub -h localhost -t wmbusmeters_alarm -m "$ALARM_TYPE $ALARM_MESSAGE"
# The alarmtimeout and expected activity is also used to detect failing receiving radio hardware.
#alarmtimeout=1h
#alarmexpectedactivity=mon-sun(00-23)
```

##### subscribe MQTT topic from host
- mosquitto_sub -h localhost -t "wmbusmeters/51035726" | tee test.txt

##### handling container with shell
docker exec -it wmbusmeters /bin/sh
Press Ctrl+P, Ctrl+Q to detach without stopping the container.

##### finding the dongle instead of device=auto:t1 mode
ls /dev/ttyUSB* /dev/ttyACM*    --> list attached stick
lsusb                           --> Bus 001 Device 006: ID 04b4:0003 Cypress Semiconductor Corp. iU891A
ls -l /dev/serial/by-id/        --> show symbolic link to dongle
journalctl -k -n 50 | grep tty  --> check when dongle was attached

## TODO
- [ ] change auto detection to correct dongle
  - Started auto iu891a[00202071] on /dev/ttyACM0 listening on t1
  - issues with finding it. see conf file what all have been tried
  - auto works fine though ¯\\_(ツ)_/¯
  - get current setup: scp root@192.168.176.147:/opt/wmbusmeters/common.zip .
    - (needs apt install openssh-sftp-server)
- [ ] setup using docker compose
- [x] run without --privileged mode
docker run -d \
    --name=wmbusmetersdirect \
    --restart=always \
    -v /etc/localtime:/etc/localtime:ro \
    -v /opt/wmbusmeters:/wmbusmeters_data \
    --device=/dev/ttyACM0 \
    wmbusmeters/wmbusmeters
- [ ] setup password for MQTT



# Docker Compose Multi-Container Application
- docker-compose.yml
```
services:
  wmbusmeterscomp:
    image: wmbusmeters/wmbusmeters
    container_name: wmbusmeterscomp
    restart: always
    volumes:
      - /opt/wmbusmeterscomp:/wmbusmeters_data
      - /etc/localtime:/etc/localtime:ro
    devices:
      - /dev/ttyACM0
```
- docker-compose up -d
- docker-compose down



# Installation using snap
sudo snap install wmbusmeters

sudo snap connect wmbusmeters:raw-usb core:raw-usb
sudo snap connect wmbusmeters:system-observe core:system-observe

sudo snap services wmbusmeters
sudo snap restart wmbusmeters

/var/snap/wmbusmeters/common/etc/
/var/snap/wmbusmeters/common/logs/

## Monitoring

##### Status summary
systemctl status snap.wmbusmeters.*
##### Status summary (live)
watch systemctl status snap.wmbusmeters.*
##### Service log:
journalctl -u snap.wmbusmeters.*


# MQTT

## Installation
sudo apt update
sudo apt install mosquitto
sudo apt install mosquitto-clients
sudo systemctl start mosquitto
sudo systemctl enable mosquitto


##### Pub in wmbusmeters.conf
shell=/usr/bin/mosquitto_pub -h localhost -t wmbusmeters/$METER_ID -m "$METER_JSON"
##### Sub
mosquitto_sub -h localhost -t "wmbusmeters/51035693" | tee test.txt