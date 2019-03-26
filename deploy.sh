eval "$(ssh-agent -s)" &&
ssh-add -k ~/.ssh/id_rsa &&
cd /home/ubuntu/ecommerce_project/ProjectPortofolio
git pull

source ~/.profile
echo "DOCKERHUB_PASS" | docker login --username $DOCKERHUB_USER --password-stdin
# sudo killall docker-containerd-shim
docker stop bukuku
docker rm bukuku
docker rmi dindakartika/bukuku
docker run -d --name bukuku -p 5000:5000 dindakartika/bukuku:latest
