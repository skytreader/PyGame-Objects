FROM ubuntu:16.04
COPY . ./PyGame-Objects
WORKDIR ./PyGame-Objects

RUN apt-get update
RUN apt-get install -y mercurial libfreetype6-dev python-pip
RUN apt-get build-dep -y python-pygame
RUN pip install hg+http://bitbucket.org/pygame/pygame

CMD ./docker_keepalive
