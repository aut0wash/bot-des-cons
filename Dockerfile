FROM debian:latest

ENTRYPOINT ["/usr/bin/python3.5", "-u", "main.py"]

WORKDIR /root/discord

RUN apt-get update
RUN apt-get install -y libffi-dev python3-pip python3.5-dev

COPY requirements.txt .

RUN python3 -m pip install -U -r /root/discord/requirements.txt

COPY source .
