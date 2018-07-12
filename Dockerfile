FROM ubuntu:latest
RUN apt-get update
RUN apt-get install  -y software-properties-common debconf-utils
RUN apt-get update -y

RUN apt-get install -y python-pip python-dev build-essential



ENV JAVA_VER 10
ENV JAVA_HOME /usr/lib/jvm/java-10-oracle



RUN add-apt-repository -y ppa:linuxuprising/java && \
    apt-get update -y &&\
    echo debconf shared/accepted-oracle-license-v1-1 select true | debconf-set-selections && \
    echo debconf shared/accepted-oracle-license-v1-1 seen true | debconf-set-selections &&\
    apt-get install  -y oracle-java10-installer

#RUN apt-get install -y oracle-java10-set-default
COPY . /App
WORKDIR /App
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]