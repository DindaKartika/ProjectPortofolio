eval "$(ssh-agent -s)" &&
ssh-add -k ~/.ssh/id_rsa &&
cd /home/ubuntu/ecommerce_project/ProjectPortofolio
git pull

source /root/.profile
sudo echo "DOCKERHUB_PASS" | sudo docker login --username $DOCKERHUB_USER --password-stdin
sudo docker stop bukuku
sudo docker rm bukuku
sudo docker rmi dindakartika/bukuku
sudo docker run -d --name bukuku -p 5000:5000 dindakartika/bukuku:latest
