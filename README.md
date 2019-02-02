# metermaid-docker

Here it is, metermaid all wrapped into one docker-container.

Step 1:

Purchase SDR

Step 2:
`git clone this repo`

edit ./weather/code/weather.py, and change the url parameters, currently it's using my free api key. Feel free to use mine while testing, but they are free so if you like it, please use your own key.


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

while running, create the database we nee
