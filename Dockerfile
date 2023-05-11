FROM alpine:3.18
EXPOSE 3031
VOLUME /usr/src/app/
WORKDIR /usr/src/app/
RUN apk add --no-cache \
        python3 \
        python3-dev \
        gcc \
        g++ \
        libc-dev \
        py3-pip
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
RUN python3 src/generateColor.py
ARG FLASK_APP=server.py
CMD ["flask", "run"]
