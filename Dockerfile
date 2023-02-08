FROM python:3.11-buster
LABEL maintainer "chadestioco@gmail.com"

RUN apt-get update && \
    apt-get install -y python3-pygame

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
COPY ./ app/
RUN cd app/ && python setup.py install
RUN useradd -m -U -s /bin/bash pygame

USER pygame
WORKDIR /home/pygame
ENV SHELL /bin/bash

CMD /bin/bash
