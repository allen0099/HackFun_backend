# Project

### Requirements

Docker and docker-compose  
Python version: 3.7+  
Package listed in `requirements.txt`
    
### Install

testing at Ubuntu 18.04  
```shell script
# clone the project
git clone git@github.com:allen0099/TKU-project
cd TKU-project

# intsall python 3.7
sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.7 python3.7-dev python3.7-venv python3.7-doc binfmt-support
# intsall mysql requirements
sudo apt install libmysqlclient-dev mysql-server
# add vitural environment
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
# copy and edit project config
cp credentials.example.ini credentials.ini
vim credentials.ini
# build database
chmod +x startFlaskShell.sh
./startFlaskShell.sh
>>> db.create_all()
>>> exit
# start the server
chmod +x startFlaskServer.sh
./startFlaskServer.sh
```
> **WARNING**: listen at 0.0.0.0 may cause some horrible problem, use at your own risk
```shell script
# using uwsgi
uwsgi --socket 0.0.0.0:8080 --protocol=http --master --enable-threads -w wsgi:application --processes 4
```
To make it available when system boot up
```shell script
sudo cp ./docker/backend.service /etc/systemd/system/backend.service
sudo systemctl start backend.service
sudo systemctl enable backend.service

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

### Contribute

[AngularJS Git Commit Message Conventions](https://docs.google.com/document/d/1QrDFcIiPjSLDn3EL15IJygNPiHORgU1_OOAqWjiDU5Y/edit#heading=h.greljkmo14y0)

### Contact

[allen0099](https://t.me/allen0099)
