FROM ubuntu:latest
RUN apt-get update && apt-get install -y git python build-essential python-pip python-dev curl wget
RUN (wget -O - pi.dk/3 || curl pi.dk/3/) | bash
RUN pip install scipy
RUN pip install gensim
RUN pip install pyro4
WORKDIR /usr/local/share
RUN git clone https://github.com/brian-cleary/LatentStrainAnalysis
WORKDIR /usr/local/share/LatentStrainAnalysis
RUN tar -xzf testData.tar.gz
