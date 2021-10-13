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
    apt-get clean && \
    git clone https://github.com/pcercuei/libini.git && cd libini && mkdir build && cd build && cmake ../ && make && make install && cd && \
    git clone https://github.com/analogdevicesinc/libiio.git && cd libiio && mkdir build && cd build && cmake ../ -DPYTHON_BINDINGS=ON && make && make install && cd

# install python iio with other library
# https://wiki.analog.com/resources/tools-software/linux-software/pyadi-iio
ENV PYTHONPATH=$PYTHONPATH:/usr/lib/python${PYTHONVER}/site-packages
RUN python${PYTHONVER} -m pip install pylibiio pyadi-iio matplotlib numpy scipy

# install gnu-radio with gr-iio
# https://wiki.analog.com/resources/tools-software/linux-software/pyadi-iio
RUN \
    apt-get install gnuradio -y && \
    git clone https://github.com/analogdevicesinc/libad9361-iio.git && cd libad9361-iio && cmake . && make && make install && cd && \
    apt-get install bison flex cmake git libgmp-dev swig liborc-dev -y && \
    git clone -b upgrade-3.8 https://github.com/analogdevicesinc/gr-iio.git && cd gr-iio && cmake . && make && make install && cd && ldconfig && \
    apt-get clean
ENV PYTHONPATH=$PYTHONPATH:/usr/lib/python${PYTHONVER}/dist-packages