# Project

### Requirements

Docker and docker-compose  
Python version: 3.7+  
Package listed in `requirements.txt`
    
### Install

testing at Ubuntu 18.04  
> clone the project
```shell script
git clone git@github.com:allen0099/backend
cd backend
```
> setup python3 virtual environment
```shell script
sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.7 python3.7-dev python3.7-venv python3.7-doc binfmt-support
# install mysql requirements
sudo apt install libmysqlclient-dev mysql-server

python3.7 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
> MySQL database docker compose
```shell script
./docker/startDockerCompose.sh
```
> Flask shell
```shell script
cd ./sh
./startFlaskShell.sh
>>> db.create_all()
>>> exit
# start the server
./startFlaskServer.sh
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
```shell script
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
