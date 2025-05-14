Delivery FastAPI service with DDD architecture
========================================


## RUN


### Requierd
    python 3.11

### Venv installation

    python3 -m venv venv

### Requirements installation

```sh

source venv/bin/activate
pip install --no-cache-dir --upgrade -r requirements.txt
```


```sh
source venv/bin/activate
fastapi run main.py --host 1.0.0.127 --port 8000
```

### By docker compose

For ```delivery cervise``` runs at 8855 port create ```docker compose``` file with below image description.
At the `.env` file  should be provided value of `CI_REGISTRY`:

```sh

  delivery:
    image: ${CI_REGISTRY}/delivery:latest
    restart: always
    ports:
      - "8855:8000"
    env_file:
      - ./.env


```

For image update at the registry you should create local image by:

```sh
docker build -t delivery:latest .

docker tag delivery:latest github.com/pavelkalininn/delivery:latest

docker push github.com/pavelkalininn/delivery:latest
```