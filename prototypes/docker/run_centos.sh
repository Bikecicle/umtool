
#!/bin/sh
sudo docker run -dit --name docker-centos --hostname="centos" centos
sudo docker attach docker-centos
