
## Colector + exporter

### Instalar la base para autoinstrumentar
```yaml
# /tmp/otel-collector-config.yaml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318
exporters:
  # NOTE: Prior to v0.86.0 use `logging` instead of `debug`.
  debug:
    verbosity: detailed
  otlp:
    endpoint: "jaeger:4317"
    tls:
      insecure: true
  otlphttp/prometheus:
    endpoint: "http://prometheus:9090/api/v1/otlp"
    tls:
      insecure: true
processors:
  batch:
service:
  pipelines:
    traces:
      receivers: [otlp]
      exporters: [otlp, debug]
      processors: [batch]
    metrics:
      receivers: [otlp]
      exporters: [otlphttp/prometheus, debug]
      processors: [batch]
    logs:
      receivers: [otlp]
      exporters: [debug]
      processors: [batch]
```

```bash
rm /tmp/otel-collector-config.yaml
ln -s $PWD/otel-collector-configv2.yaml /tmp/otel-collector-config.yaml
```

### crear una red en docker
```bash
docker network create devops
```

### Subir prometheus

#### Archivo de conf prometheus
```yaml
# /tmp/prometheus/prometheus-config.yaml
global:
  scrape_interval: 5s
  scrape_timeout: 3s
  evaluation_interval: 30s

otlp:
  promote_resource_attributes:
    - service.instance.id
    - service.name
    - service.namespace
    - cloud.availability_zone
    - cloud.region
    - container.name
    - deployment.environment.name

storage:
  tsdb:
    out_of_order_time_window: 30m
```

```bash
mkdir -p /tmp/prometheus
ln -s $PWD/prometheus-config.yaml /tmp/prometheus/prometheus-config.yaml

docker run -p 9090:9090 --rm --name prometheus --network devops \
  -v /tmp/prometheus/prometheus-config.yaml:/etc/prometheus/prometheus-config.yaml \
  quay.io/prometheus/prometheus:v3.2.0 \
  --web.console.templates=/etc/prometheus/consoles \
  --web.console.libraries=/etc/prometheus/console_libraries \
  --storage.tsdb.retention.time=1h \
  --config.file=/etc/prometheus/prometheus-config.yaml \
  --storage.tsdb.path=/prometheus \
  --web.enable-lifecycle \
  --web.route-prefix=/ \
  --web.enable-otlp-receiver \
  --enable-feature=exemplar-storage
```

### Subir jaeger
```bash
docker run -p 16686:16686 --rm --name jaeger --network devops --env METRICS_STORAGE_TYPE=prometheus \
  docker.io/jaegertracing/all-in-one:1.66.0 \
  --memory.max-traces=5000 \
  --query.base-path=/jaeger/ui \
  --prometheus.server-url=http://prometheus:9090 \
  --prometheus.query.normalize-calls=true \
  --prometheus.query.normalize-duration=true
```

### Lanzar el colector
```bash
docker run -p 4317:4317 --rm --name opentelemetry-colector --network devops \
    -v /tmp/otel-collector-config.yaml:/etc/otel-collector-config.yaml \
    docker.io/otel/opentelemetry-collector:latest \
    --config=/etc/otel-collector-config.yaml
```


### Instalar el exporter para la app
```bash
pip install opentelemetry-exporter-otlp
```

### Ejecutar la app instrumentada
```bash
export OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true
opentelemetry-instrument --logs_exporter otlp flask run -p 8080
```


### Verificar la app
http://localhost:8080/lanzardado

### Lanzar por navegador o por curl
```bash
# Anonimo
curl -X GET http://localhost:8080/lanzardado
# Player uno
curl -X GET http://localhost:8080/lanzardado?jugador=uno
```

### Verificar en prometheus
http://localhost:9090/

### Verificar en jaeger
http://localhost:16686/

