FROM hmlandregistry/dev_base_python:3

RUN yum install -y -q postgresql-devel

ENV SQL_HOST=postgres \
  SQL_DATABASE=search_api_db \
  SQL_USERNAME=maintain_feeder_user \
  SQL_PASSWORD=password \
  SQLALCHEMY_POOL_SIZE=10 \
  APP_NAME=maintain-feeder \
  EXCHANGE_NAME=llc-charge-exchange \
  EXCHANGE_TYPE=topic \
  RABBIT_URL=amqp://guest:guest@rabbitmq:5672// \
  QUEUE_NAME=maintain_feeder_queue \
  ERROR_QUEUE_NAME=maintain_feeder_error \
  ROUTING_KEYS="llc-maintain;llc.*" \
  RPC_ROUTING_KEY="llc-maintain-rpc" \
  RPC_QUEUE_NAME="maintain_feeder_rpc" \
  RPC_EXCHANGE_NAME="llc_feeder_rpc" \
  MAX_MSG_RETRY="1" \
  REGISTER_URL=http://register:8080 \
  KOMBU_LOG_LEVEL=INFO \
  LOG_LEVEL=DEBUG \
  SQLALCHEMY_POOL_RECYCLE="3300"

WORKDIR /src
ENV PYTHONPATH /src
CMD ["python3", "/src/manage.py", "runserver"]

ADD requirements_test.txt requirements_test.txt
ADD requirements.txt requirements.txt
RUN pip3 install -q -r requirements.txt && \
    pip3 install -q -r requirements_test.txt
