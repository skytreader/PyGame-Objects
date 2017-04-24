FROM ubuntu:16.04
LABEL maintainer "chadestioco@gmail.com"

ADD ./requirements.txt ./requirements.txt

RUN apt-get update --fix-missing
RUN apt-get install -y python-pygame python-pip
RUN pip install -r requirements.txt
RUN useradd -m -U -s /bin/bash pygame

USER pygame
WORKDIR /home/pygame
ENV SHELL /bin/bash

CMD /bin/bash
