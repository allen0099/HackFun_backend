# Project

### Requirements

Docker and docker-compose  
Python version: 3.7+  
Package listed in `requirements.txt`
    
### Install

testing at Ubuntu 18.04  
```shell script
# clone the project
git clone git@github.com:allen0099/backend
cd backend

# intsall python 3.7
sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.7 python3.7-dev python3.7-venv python3.7-doc binfmt-support
# intsall mysql requirements
sudo apt install libmysqlclient-dev mysql-server

# create vitural environment
python3.7 -m venv venv
# activate vitural environment
source venv/bin/activate
# install requirements.txt
pip install -r requirements.txt

# edit the docker config
vim ./docker/project.yml
# make sure you have docker and docker-compose already
chmod +x ./docker/startDockerCompose.sh
./docker/startDockerCompose.sh

# build database
chmod +x startFlaskShell.sh
./startFlaskShell.sh
>>> db.create_all()
>>> from app.models import *
>>> exit
# start the server
chmod +x ./sh/startFlaskServer.sh
./sh/startFlaskServer.sh
```
> **WARNING**: listen at 0.0.0.0 may cause some horrible problem, use at your own risk
```shell script
# using uwsgi
uwsgi --socket 0.0.0.0:8080 --protocol=http --master --enable-threads -w wsgi:application --processes 4
```
> To make it available when system up
```shell script
sudo cp ./docker/backend.service /etc/systemd/system/backend.service
sudo systemctl start backend.service
sudo systemctl enable backend.service
```
> setup nginx config
```
# edit nginx config
sudo cp backend /etc/nginx/sites-available/backend
sudo ln -s /etc/nginx/sites-available/backend /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

recommend using PyCharm for IDE  
plugins:  
[Git Commit Template](https://plugins.jetbrains.com/plugin/9861-git-commit-template/)  
[GitToolBox](https://plugins.jetbrains.com/plugin/index?xmlId=zielu.gittoolbox)

### Contact

[allen0099](https://t.me/allen0099)
