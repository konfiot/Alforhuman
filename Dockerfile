FROM alpine:3.7
EXPOSE 3031
VOLUME /usr/src/app/
WORKDIR /usr/src/app/
RUN apk add --no-cache \
        python3
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
RUN python3 src/generateColor.py
ARG FLASK_APP=server.py
CMD ["flask", "run"]
