FROM ubuntu:16.04
COPY . ./PyGame-Objects
WORKDIR ./PyGame-Objects

RUN apt-get update --fix-missing
RUN apt-get install -y mercurial libfreetype6-dev python-pip
RUN apt-get install -y python-pygame

CMD /bin/bash
