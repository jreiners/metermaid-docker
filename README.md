# metermaid-docker

Here it is, metermaid all wrapped into one docker-container.

Step 1:

Purchase SDR, and plug into PC's usb port.

Step 2:
clone this repo.

edit ./weather/code/weather.py, and change the url parameters, currently it's using my free api key, and an omaha location. Feel free to use mine while testing, but they are free so if you like it, please use your own key.


Step 3:

The docker-compose script will create a database for everything to use.


To run:

you need docker, and docker-compose installed

on redhat:

```
yum install -y docker docker-compose
systemctl start docker && systemctl enable docker
cd ./metermaid
docker-compose up -d

```

It exposes a few ports on the host side.

3306- mysql - root:weatherdb
3000 - grafana admin:admin

All app storage is persistant, you can change the password for grafana, and it'll stick between rebuilds. You can also change the mysql username, but my scripts default to that user so you might need to fix a few things.


