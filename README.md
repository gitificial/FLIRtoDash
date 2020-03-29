# FLIRtoDash
Dash webapp to get some statistics from pixel values of an image (saved as CSV). The statistics are calculated over a selected region of interest (ROI). The app was intended to get some statistics from thermographic images from a FLIR camera, but can be used for other types of images as well.

![FLIRtoDash screenshot](https://github.com/gitificial/FLIRtoDash/blob/master/screenshot.png)


## Installation
The following instructions describe the installation process on a linux system and might deviate to the installation on Windows/macOS.

### Install the Docker image containing the webapp
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
sudo docker run -itd --network=multi-host-network --ip 172.20.0.2 ubuntu_image
```
The webapp is now reachable with a browser through http://172.20.0.2:8050 .

### ...

Files overview:
**flirToDash.py** - Dash webapp
**Dockerfile** - Dockerfile to create a Ubuntu Docker image with the webapp


