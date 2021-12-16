FROM ubuntu:latest
RUN apt-get update && apt-get install -y python2.7 python-dev python-pip vowpal-wabbit git wget curl
RUN pip install sklearn
RUN pip install pandas
WORKDIR /usr/local/share
RUN git clone https://github.com/yunwilliamyu/opal.git
