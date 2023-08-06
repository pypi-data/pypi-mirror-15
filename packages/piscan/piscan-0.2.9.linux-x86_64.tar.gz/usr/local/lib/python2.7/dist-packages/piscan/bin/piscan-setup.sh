#!/bin/bash
echo "*** Starting Setup ***" >> /tmp/piscansetup.log

echo "*** Installing Required Components ***" >> /tmp/piscansetup.log

# b8:27:eb:2c:9c:1b - 192.168.0.113 - PiScan 1 (Top)
# b8:27:eb:6b:e4:fe - 192.168.0.109 - PiScan 2 (Middle)
# b8:27:eb:1a:ed:f1 - 192.168.0.111 - PiScan 3 (Bottom)

SysMac = "$(cat /sys/class/net/eth0/address)"
if [$SysMac = "b8:27:eb:2c:9c:1b"]; then
    echo "PiScan1" > /etc/hostname
fi
if [$SysMac = "b8:27:eb:6b:e4:fe"]; then
    echo "PiScan2" > /etc/hostname
fi
if [$SysMac = "b8:27:eb:1a:ed:f1"]; then
    echo "PiScan3" > /etc/hostname
fi

echo "[global]" > /etc/piscan/piscan.ini
echo "qtype: sqs" > /etc/piscan/piscan.ini
echo "region: us-east-1" > /etc/piscan/piscan.ini
echo "store: cuts" > /etc/piscan/piscan.ini
echo "queue: Inbound" > /etc/piscan/piscan.ini
echo "" > /etc/piscan/piscan.ini
echo "[account]" > /etc/piscan/piscan.ini
echo "id: AKIAIRB443KH6BYRQTWA" > /etc/piscan/piscan.ini
echo "secret: 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" > /etc/piscan/piscan.ini
echo "hash: a457529c4fc8ca95e65012a109661826" > /etc/piscan/piscan.ini

if [$SysMac = "b8:27:eb:2c:9c:1b"]; then
    echo "RID: 1" > /etc/piscan/piscan.ini
fi
if [$SysMac = "b8:27:eb:6b:e4:fe"]; then
    echo "RID: 2" > /etc/piscan/piscan.ini
fi
if [$SysMac = "b8:27:eb:1a:ed:f1"]; then
    echo "RID: 3" > /etc/piscan/piscan.ini
fi
echo "UID: 1" > /etc/piscan/piscan.ini
echo "" > /etc/piscan/piscan.ini
echo "[system]" > /etc/piscan/piscan.ini
echo "logloc: /var/log" > /etc/piscan/piscan.ini
echo "serialport: /dev/ttyUSB0" > /etc/piscan/piscan.ini
echo "baudrate: 115200" > /etc/piscan/piscan.ini
echo "tmpfileloc: /tmp" > /etc/piscan/piscan.ini
echo "audiodevice: hw:1,0" > /etc/piscan/piscan.ini
echo "bitrate: 48000" > /etc/piscan/piscan.ini

sudo apt-get update
sudo apt-get -q -y install sox
sudo apt-get -q -y install lame
sudo apt-get -q -y install rabbitmq-server
 
sudo pip install flask

sudo mkdir /etc/piscan
Y
# Move initial boto.cfg
sudo cp /usr/local/lib/python2.7/dist-packages/piscan/data/boto.cfg /etc/boto.cfg

# Create piscan.ini file
#sudo cp /usr/local/lib/python2.7/dist-packages/piscan/data/piscan.ini /etc/piscan/piscan.ini

# Run a ls /dev/tty* to check for the serial port

# Copy init.d service entries to /etc/init.d for auto start of services
sudo cp /usr/local/lib/python2.7/dist-packages/piscan/data/piqueue.sh /etc/init.d/piqueue.sh
sudo cp /usr/local/lib/python2.7/dist-packages/piscan/data/pirec.sh /etc/init.d/pirec.sh
sudo cp /usr/local/lib/python2.7/dist-packages/piscan/data/piwi.sh /etc/init.d/piwi.sh

sudo chmod 755 /usr/local/lib/python2.7/dist-packages/piscan/pirec.py
sudo chmod 755 /usr/local/lib/python2.7/dist-packages/piscan/piqueue.py
sudo chmod 755 /usr/local/lib/python2.7/dist-packages/piscan/frontend/piwi.py
sudo chmod 755 /etc/init.d/piqueue.sh
sudo chmod 755 /etc/init.d/pirec.sh
sudo chmod 755 /etc/init.d/piwi.sh

sudo update-rc.d piqueue.sh defaults
sudo update-rc.d pirec.sh defaults
sudo update-rc.d piwi.sh defaults

# Reboot?

# Check sound levels
# Turn ALSA Mixer on/up
# sudo alsamixer
# F5 to set ALL
# F6 to selecte soundcard (Select USB)
#sudo alsactl store

