FROM ubuntu:22.04

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/London

RUN apt update -q \
 && apt upgrade -yq \
 && apt install -y -qq tzdata bash build-essential lame libpq-dev wget supervisor \
    festival festival-dev python3 python3-pip python3-setuptools python3-dev \
 && python3 -m pip install --upgrade pip \
 && apt clean -q
 
WORKDIR /usr/share/festival/voices/
RUN wget -c https://github.com/techiaith/llais_festival/archive/v1.1.0.tar.gz -O - | tar -xz

WORKDIR /festival

COPY ./app/requirements.txt /festival/requirements.txt
RUN python3 -m pip install --no-cache-dir -r /festival/requirements.txt

COPY ./app /festival/

EXPOSE 8008

CMD supervisord -c /festival/supervisord.conf -n

