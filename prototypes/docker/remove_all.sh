#!/bin/sh
docker stop $(docker ps -aq)
sudo docker rm $(sudo docker ps -a -q)
sudo docker rmi $(sudo docker images -q)
