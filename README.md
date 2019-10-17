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
sudo apt install python-3.7 python-3.7-dev python3.7-venv python3.7-doc binfmt-support
# intsall mysql requirements
sudo apt install libmysqlclient-dev mysql-server

# make sure you have docker and docker-compose already
chmod +x ./docker/startDockerCompose.sh
./docker/startDockerCompose.sh

# add vitural environment
python3.7 -m venv venv
# activate vitural environment
source venv/bin/activate
# install requirements.txt
pip install -r requirements.txt
# start the server
chmod +x startFlaskServer.sh
./startFlaskServer.sh
```

recommend using PyCharm for IDE  
plugins:  
[Git Commit Template](https://plugins.jetbrains.com/plugin/9861-git-commit-template/)  
[GitToolBox](https://plugins.jetbrains.com/plugin/index?xmlId=zielu.gittoolbox)

### Contribute

[AngularJS Git Commit Message Conventions](https://docs.google.com/document/d/1QrDFcIiPjSLDn3EL15IJygNPiHORgU1_OOAqWjiDU5Y/edit#heading=h.greljkmo14y0)

### Contact

[allen0099](https://t.me/allen0099)
