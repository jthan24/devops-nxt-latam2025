
## Colector

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
processors:
  batch:
service:
  pipelines:
    traces:
      receivers: [otlp]
      exporters: [debug]
      processors: [batch]
    metrics:
      receivers: [otlp]
      exporters: [debug]
      processors: [batch]
    logs:
      receivers: [otlp]
      exporters: [debug]
      processors: [batch]
```

### Hacer un link simbolico para /tmp
```bash
ln -s $PWD/otel-collector-config.yaml /tmp/
```

### Lanzar el colector
```bash
docker run -p 4317:4317 --rm --name opentelemetry-colector \
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

