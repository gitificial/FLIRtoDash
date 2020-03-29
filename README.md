# FLIRtoDash
[Dash](https://plotly.com/dash/) webapp to get some statistics from pixel values of an image (saved as CSV). The statistics are calculated over a selected region of interest (ROI). The app was intended to get some statistics from thermographic images from a FLIR camera, but can be used for other types of images as well.

![FLIRtoDash screenshot](https://github.com/gitificial/FLIRtoDash/blob/master/screenshot.png)


## Installation
The following instructions describe two installation options on a linux system and might deviate to the installation on Windows/macOS.

### Option 1: Install the Docker image containing the webapp
Get the Docker image from Docker Hub:
```bash
sudo docker pull dockificial/ubuntu_flirtodash:latest
```
Create a local Docker network:
```bash
sudo docker network create --subnet 172.20.0.0/24 multi-host-network
```
Create and run a container. The container is attached to the network with the IP 172.20.0.2:
```bash
sudo docker run -itd --network=multi-host-network --ip 172.20.0.2 dockificial/ubuntu_flirtodash:latest
```
The webapp is now reachable with a browser through http://172.20.0.2:8050 .

### Option 2: Webapp installation on an Ubuntu Server image to run as VM in VirtualBox
1. Download [Ubuntu Server](https://ubuntu.com/download/server) iso image.
2. Create a VirtualBox VM with the iso.
3. Install the following packages:
```bash
sudo apt-get -y install virtualenv python3-pip unzip tmux
```
4. Create a virtual environment and enter it:
```bash
virtualenv venv -p python3
source venv/bin/activate
```
5. Set empty PYTHONPATH environment variable:
```bash
export PYTHONPATH=
```
6. Install necessary Python3 packages:
```bash
pip3 install --upgrade pip --user
pip3 install numpy
pip3 install pandas
pip3 install scipy
pip3 install dash
pip3 install dash_bootstrap_components
```
7. Download and uncompress FLIRtoDash app:
```bash
cd
mkdir flir
cd flir
wget https://github.com/gitificial/FLIRtoDash/archive/master.zip
unzip master.zip
```
8. Add a new cronjob to start the webapp at boot time. Open the cronjob file with the command "crontab -e" and add following line to the very end:
```bash
@reboot tmux new-session -d -s "flirSession" $HOME/flir/FLIRtoDash-master/flir_start.sh
```
9. Reboot the system. The webapp is now reachable on http://UBUNTU_SERVER_IP:8050


### Files overview:
**flirToDash.py** - Dash webapp<br/>
**Dockerfile** - Dockerfile to create a Ubuntu Docker image with the webapp<br/>
**example.csv** - Thermographic image as CSV. Each table cell contains the temperature of it's corresponding pixel.


