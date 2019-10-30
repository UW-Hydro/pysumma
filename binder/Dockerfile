## SUMMA and pySUMMA binder

FROM ubuntu:xenial

# install only the packages that are needed
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
     software-properties-common python-software-properties \ 
    ca-certificates \
    git \
    make \
    libnetcdff-dev \
    liblapack-dev \
    vim \
    zip \
    unzip \ 
    python3 \
    python3-pip


# install gfortran-6
RUN add-apt-repository ppa:ubuntu-toolchain-r/test -y \
    && apt-get update \
    && apt-get install -y --no-install-recommends gfortran-6 \
    && apt-get clean

COPY summa/* ./

# set environment variables for docker build
ENV F_MASTER /code/summa
ENV FC gfortran
ENV FC_EXE gfortran
ENV FC_ENV gfortran-6-docker

# add code directory
WORKDIR /code
ADD . /code

# fetch tags and build summa
RUN git fetch --tags && make -C /code/summa/build/ -f Makefile

RUN pip3 install --upgrade pip setuptools wheel 
RUN git clone https://github.com/uva-hydroinformatics/pysumma.git 
RUN cd pysumma && pip3 install .

RUN pip3 install --no-cache --upgrade pip && \
    pip3 install --no-cache notebook

# create user with a home directory
ARG NB_USER
ARG NB_UID
ENV USER ${NB_USER}
ENV HOME /home/${NB_USER}

RUN adduser --disabled-password \
    --gecos "Default user" \
    --uid ${NB_UID} \
    ${NB_USER}
WORKDIR ${HOME}
USER ${USER}

COPY notebook/* ./