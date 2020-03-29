# FLIRtoDash
Dash webapp to get some statistics from pixel values of an image (saved as CSV). The statistics are calculated over a selected region of interest (ROI). The app was intended to get some statistics from thermographic images from a FLIR camera, but can be used for other types of images as well.




## Installation
```bash
sudo docker pull dockificial/ubuntu_flirtodash:latest
```

Files overview:
**flirToDash.py** - Dash webapp
**Dockerfile** - Dockerfile to create a Ubuntu Docker image with the webapp


