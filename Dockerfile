FROM ubuntu:16.04
LABEL maintainer "chadestioco@gmail.com"

COPY ./ app/

RUN apt-get update --fix-missing
RUN apt-get install -y python-pygame python-pip
RUN pip install -r /app/requirements.txt
RUN cd app/ && python setup.py install
RUN useradd -m -U -s /bin/bash pygame

USER pygame
WORKDIR /home/pygame
ENV SHELL /bin/bash

CMD /bin/bash
