From centos:7
RUN yum -y update
RUN yum -y install wget vim tar epel-release git nc && yum -y install rtl-sdr python34 python34-mysql python34-pip
RUN wget https://dl.google.com/go/go1.10.1.linux-amd64.tar.gz
RUN tar -xf go1.10.1.linux-amd64.tar.gz && mv go /usr/local/
RUN mkdir /projects/
RUN mkdir -p /app/bin && cd /app/bin
ENV GOROOT=/usr/local/go
ENV GOPATH=/projects 
ENV PATH=$GOPATH/bin:$GOROOT/bin:$PATH:/app/bin/MeterMaid
COPY code /app/bin/
RUN ln -s /usr/bin/python3.4 /usr/bin/python3
RUN python3 -m pip install pymysql mysql-connector-python simplejson mysql-connector requests
ENTRYPOINT bash /app/bin/run.sh 

