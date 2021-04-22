# commands

First you need to train model
```bash
python train.py
```

```bash 
docker-compose up --build
```

```bash
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"flower":"1,2,3,6"}' \
  http://localhost:5000/iris_post
```
