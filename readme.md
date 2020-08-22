# commands

sudo docker exec -it web-service_flask_1 bash

sudo docker exec -it web-service_flask_1 python train.py

curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"flower":"1,2,3,6"}' \
  http://localhost:5000/iris_post