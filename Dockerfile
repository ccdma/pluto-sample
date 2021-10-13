# 2021/10/13 by face0u0

FROM ubuntu:focal-20210921

ARG PYTHONVER=3.8

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update

# install libiio　(with python bindings)
# https://github.com/analogdevicesinc/libiio/blob/master/README_BUILD.md
RUN \
    apt-get install build-essential -y && \
    apt-get install libxml2-dev bison flex libcdk5-dev cmake git -y && \
    apt-get install libaio-dev libusb-1.0-0-dev -y && \
    apt-get install libserialport-dev libavahi-client-dev -y && \
    apt-get install doxygen graphviz -y && \
    apt-get install python${PYTHONVER} python3-pip python3-setuptools -y && \
    apt-get clean
RUN \
    git clone https://github.com/pcercuei/libini.git && cd libini && mkdir build && cd build && cmake ../ && make && make install && cd && \
    git clone https://github.com/analogdevicesinc/libiio.git && cd libiio && mkdir build && cd build && cmake ../ -DPYTHON_BINDINGS=ON && make && make install && cd
ENV PYTHONPATH=$PYTHONPATH:/usr/lib/python${PYTHONVER}/site-packages

# install python iio
# https://wiki.analog.com/resources/tools-software/linux-software/pyadi-iio
RUN python${PYTHONVER} -m pip install pylibiio pyadi-iio matplotlib numpy scipy

