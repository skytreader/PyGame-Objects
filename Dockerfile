FROM ubuntu:16.04
LABEL maintainer "chadestioco@gmail.com"
COPY . /home/pygame/PyGame-Objects
WORKDIR /home/pygame/PyGame-Objects

RUN apt-get update --fix-missing
RUN apt-get install -y python-pygame
RUN useradd -m -U -s /bin/bash pygame
RUN chown -R pygame:pygame /home/pygame/PyGame-Objects

USER pygame
WORKDIR /home/pygame
ENV SHELL /bin/bash

CMD /bin/bash
