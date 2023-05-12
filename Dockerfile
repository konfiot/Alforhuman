FROM ubuntu:22.04
EXPOSE 3031
VOLUME /usr/src/app/
WORKDIR /usr/src/app/
RUN apt update && apt install python3-pip build-essential
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
RUN python3 src/generateColor.py
ARG FLASK_APP=server.py
CMD ["flask", "run"]
