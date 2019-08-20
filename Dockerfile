# docker build --tag sandbox

FROM ubuntu

RUN apt-get update 

RUN apt-get install python3-pip locales-all -y

RUN apt-get install locales -y

RUN locale-gen en_US.UTF-8 && update-locale LANG=en_US.UTF-8

ENV LC_ALL=en_US.UTF-8

ENV LANG=en_US.UTF-8

ENV LANGUAGE=en_US.UTF-8

RUN pip3 install tqdm

COPY ./scripts /scripts

# docker run -v ~/dockers/eaf:/eaf -v ~/dockers/txt:/txt sandbox python3 ./scripts/eaf2txt.py eaf txt

