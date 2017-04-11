FROM ubuntu:16.04
LABEL maintainer "chadestioco@gmail.com"

RUN apt-get update --fix-missing
RUN apt-get install -y python-pygame
RUN useradd -m -U -s /bin/bash pygame

USER pygame
WORKDIR /home/pygame
ENV SHELL /bin/bash

CMD /bin/bash
