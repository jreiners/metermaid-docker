From centos:7
RUN yum -y update
RUN yum -y install wget vim tar epel-release git nc tee tree && yum -y install rtl-sdr python34 python34-mysql python34-pip
RUN wget https://dl.google.com/go/go1.10.1.linux-amd64.tar.gz
RUN tar -xvf go1.10.1.linux-amd64.tar.gz && mv go /usr/local/
RUN mkdir /projects/
RUN mkdir -p /app/bin && cd /app/bin
ENV GOROOT=/usr/local/go
ENV GOPATH=/projects 
ENV PATH=$GOPATH/bin:$GOROOT/bin:$PATH:/app/bin/
RUN ln -s /usr/bin/python3.4 /usr/bin/python3
COPY code /app/bin/
RUN python3 -m pip install pymysql
RUN /usr/local/go/bin/go get github.com/bemasher/rtlamr
RUN python3 -m pip install mysql-connector-python simplejson mysql-connector requests
ENTRYPOINT /bin/bash run.sh
