FROM python:alpine

ADD assets/check.py /opt/resource/check
ADD assets/in.py /opt/resource/in
ADD assets/out.py /opt/resource/out

RUN chmod +x /opt/resource/check
RUN chmod +x /opt/resource/in
RUN chmod +x /opt/resource/out

# Install Git
RUN apk update && apk upgrade && \
    apk add --no-cache bash git openssh

RUN pip3 install requests