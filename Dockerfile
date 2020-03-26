# get Ubuntu 18.04 LTS image optimized for Docker
FROM ubuntu:18.04

# Update Ubuntu packages
RUN apt-get update
RUN apt-get -y upgrade

RUN apt-get -y install python3
RUN apt-get -y install python3-pip
RUN apt-get -y install nano
RUN apt-get -y install wget
RUN apt-get -y install unzip

# create user directory
RUN mkdir /home/user
# add user
RUN useradd -d /home/user user
# change user home-directory owner to user:user
RUN chown -R user:user /home/user
# set user password to password123
RUN echo "user:password123"|chpasswd

# tell docker that all future commands should run as the appuser user
USER user

# change work directory
WORKDIR /home/user

# upgrade pip3
RUN pip3 install --upgrade pip --user
RUN pip3 install numpy
RUN pip3 install pandas
RUN pip3 install scipy

RUN pip3 install dash
RUN pip3 install dash_bootstrap_components

# get flirToDash.py and run it
RUN wget https://github.com/gitificial/FLIRtoDash/archive/master.zip
RUN unzip master.zip
RUN rm master.zip
RUN cd FLIRtoDash
RUN python3 flirToDash.py





