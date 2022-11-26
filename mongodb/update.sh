sudo docker-compose down
sudo docker-compose up -d
#sudo docker exec -it mongodb mongosh -u admin -p password -f addRole.js
sudo docker exec -it mongodb mongosh -u admin -p password -f addUser.js
