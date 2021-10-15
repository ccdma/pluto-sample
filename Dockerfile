# 2021/10/13 by face0u0

FROM ubuntu:focal-20210921

ARG UID=1000
ARG GID=1000
ARG PYTHONVER=3.8

# update apt repository
RUN apt-get update

# create and change user
RUN \
    apt-get install sudo -y && \ 
    groupadd user -g ${GID} && \
    useradd -u ${UID} -g ${GID} -m -s /bin/bash -G sudo user && \
    echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
USER user

ENV DEBIAN_FRONTEND=noninteractive
RUN sudo ln -sf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime

# install libiio　(with python bindings)
# https://github.com/analogdevicesinc/libiio/blob/master/README_BUILD.md
RUN \
    sudo apt-get install build-essential -y && \
    sudo apt-get install libxml2-dev bison flex libcdk5-dev cmake git -y && \
    sudo apt-get install libaio-dev libusb-1.0-0-dev -y && \
    sudo apt-get install libserialport-dev libavahi-client-dev -y && \
    sudo apt-get install doxygen graphviz -y && \
    sudo apt-get install python${PYTHONVER} python3-pip python3-setuptools -y && \
    sudo apt-get clean && \
    cd && git clone https://github.com/pcercuei/libini.git && cd libini && mkdir build && cd build && cmake ../ && make && sudo make install && cd && \
    cd && git clone https://github.com/analogdevicesinc/libiio.git && cd libiio && mkdir build && cd build && cmake ../ -DPYTHON_BINDINGS=ON && make && sudo make install && cd

# install python iio with other library
# https://wiki.analog.com/resources/tools-software/linux-software/pyadi-iio
ENV PYTHONPATH=$PYTHONPATH:/usr/lib/python${PYTHONVER}/site-packages
RUN \
    python${PYTHONVER} -m pip install pylibiio pyadi-iio matplotlib numpy scipy && \
    sudo apt-get install python3-tk -y && \
    sudo apt-get clean 
