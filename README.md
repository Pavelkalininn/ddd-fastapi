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


For api generation by the OpenApi file do:
    
    pip install openapi-generator-cli
    cd delivery_API/adapters/http/contract
    openapi-generator-cli generate -i https://gitlab.com/microarch-ru/microservices/dotnet/system-design/-/raw/main/services/delivery/contracts/openapi.yml -g python -o . --package-name OpenApi --additional-properties classModifier=abstract --additional-properties operationResultTask=true

For grpc api generate by the protobuf file do:

    pip install grpcio
    pip install grpcio-tools
    python -m grpc_tools.protoc -I delivery_infrastructure/adapters/grpc/ --python_out=. --pyi_out=. --grpc_python_out=. delivery_infrastructure/adapters/grpc/contract.proto