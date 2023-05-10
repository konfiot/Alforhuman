FROM alpine:3.7
EXPOSE 3031
VOLUME /usr/src/app/
WORKDIR /usr/src/app/
RUN apk add --no-cache \
        #uwsgi-python3 \
        python3
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
RUN python3 src/generateColor.py
ARG FLASK_APP=server.py
#CMD [ "uwsgi", "--socket", "0.0.0.0:3031", \
#               "--uid", "uwsgi", \
#               "--plugins", "python3", \
#               "--protocol", "uwsgi", \
#               "--wsgi", "main:server" ]
CMD ["flask", "run"]
