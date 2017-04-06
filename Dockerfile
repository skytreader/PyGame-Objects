FROM ubuntu:16.04
COPY . ./PyGame-Objects
WORKDIR ./PyGame-Objects

RUN apt-get update --fix-missing
RUN apt-get install -y mercurial libfreetype6-dev python-pip
RUN apt-get install -y python-pygame
RUN useradd -m -U -s /bin/bash pygame

USER pygame
WORKDIR /home/pygame
ENV SHELL /bin/bash

CMD /bin/bash
