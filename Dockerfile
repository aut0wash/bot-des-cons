FROM ubuntu:19.10

ENTRYPOINT ["python3", "-u", "main.py"]

WORKDIR /root/discord

RUN apt-get update
RUN apt-get install -y libffi-dev libnacl-dev python3-dev python3-pip ffmpeg

RUN python3 -m pip install -U discord.py[voice]

COPY source .

COPY audios .
